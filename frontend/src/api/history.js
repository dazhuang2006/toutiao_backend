import request from './request'

export function addHistory(newsId) {
  return request.post('/history/add', { newsId })
}

export function getHistoryList(page = 1, pageSize = 10) {
  return request.get('/history/list', { params: { page, pageSize } })
}

export function deleteHistory(historyId) {
  return request.delete(`/history/delete/${historyId}`)
}

export function clearHistory() {
  return request.delete('/history/clear')
}
