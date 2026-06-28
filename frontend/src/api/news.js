import request from './request'

export function getCategories(skip = 0, limit = 100) {
  return request.get('/news/categorise', { params: { skip, limit } })
}

export function getNewsList(categoryId, page = 1, pageSize = 10) {
  return request.get('/news/list', {
    params: { categoryId, page, pageSize }
  })
}

export function getNewsDetail(id) {
  return request.get('/news/detail', { params: { id } })
}
