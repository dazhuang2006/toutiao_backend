import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm.rag import search_news


DATA_PATH = Path(__file__).resolve().parent / "rag_longnews_questions_1.json"
REPORT_PATH = Path(__file__).resolve().parent / "rag_longnews_report.json"


def load_cases(data_path: Path) -> list[dict]:
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    cases = raw.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{data_path} 中没有 cases")
    return cases


def expected_ids(case: dict) -> list[int]:
    ids = case.get("news_ids")
    if not ids:
        news_id = case.get("news_id")
        ids = [news_id] if news_id is not None else []
    return [int(x) for x in ids]


def evaluate_case(case: dict, top_ks: list[int]) -> dict:
    question = case["question"]
    expected = set(expected_ids(case))

    hits = search_news(question, limit=max(top_ks))
    top_ids = [int(hit["news_id"]) for hit in hits]
    top_scores = [round(float(hit.get("score", 0.0)), 6) for hit in hits]

    rank = None
    for idx, news_id in enumerate(top_ids, start=1):
        if news_id in expected:
            rank = idx
            break

    recall_by_k = {}
    for k in top_ks:
        hit_at_k = bool(expected.intersection(top_ids[:k]))
        recall_by_k[k] = hit_at_k

    return {
        "id": case["id"],
        "category": case.get("category", ""),
        "question": question,
        "expected_news_ids": sorted(expected),
        "rank": rank,
        "recall": recall_by_k,
        "top_news_ids": top_ids,
        "top_scores": top_scores,
    }


def print_metrics(metrics: dict, total: int) -> None:
    print("\n指标\t命中\t总数\t召回率")
    for k, item in metrics.items():
        print(
            f"Top-{k}\t{item['hits']}\t{total}\t"
            f"{item['hits']}/{total} = {item['recall_rate']:.2%}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG Top-K news recall benchmark")
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    parser.add_argument("--top-k", default="1,3,5", help="comma-separated K values")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--limit", type=int, help="only run the first N cases")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    top_ks = sorted({int(x.strip()) for x in args.top_k.split(",") if x.strip()})
    if not top_ks:
        raise ValueError("--top-k 至少需要一个数值")

    cases = load_cases(args.data)
    if args.limit:
        cases = cases[: args.limit]

    print(f"数据集: {args.data}")
    print(f"评测问题: {len(cases)}, Top-K: {top_ks}")

    detail_results = []
    started = time.perf_counter()
    for idx, case in enumerate(cases, start=1):
        result = evaluate_case(case, top_ks)
        detail_results.append(result)
        if args.verbose:
            hit_flags = " ".join(
                f"K{k}={'Y' if result['recall'][k] else 'N'}" for k in top_ks
            )
            print(f"{idx}. {hit_flags} rank={result['rank']} {case['question']}")

    elapsed = time.perf_counter() - started
    total = len(detail_results)

    metrics = {}
    for k in top_ks:
        hits = sum(1 for item in detail_results if item["recall"][k])
        metrics[k] = {
            "hits": hits,
            "total": total,
            "recall_rate": round(hits / total, 6),
        }

    category_metrics = {}
    categories = sorted({item["category"] for item in detail_results})
    for category in categories:
        category_cases = [
            item for item in detail_results if item["category"] == category
        ]
        category_metrics[category] = {}
        for k in top_ks:
            hits = sum(
                1 for item in category_cases if item["recall"][k]
            )
            category_metrics[category][k] = round(hits / len(category_cases), 6)

    report = {
        "total": total,
        "top_k": top_ks,
        "elapsed_seconds": round(elapsed, 3),
        "metrics": {str(k): v for k, v in metrics.items()},
        "category_metrics": category_metrics,
        "cases": detail_results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print_metrics(metrics, total)
    print(f"\n耗时: {elapsed:.2f}s")
    print(f"报告已保存: {args.report}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
