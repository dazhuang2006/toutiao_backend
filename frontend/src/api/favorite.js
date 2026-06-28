import request from './request'

export function checkFavorite(newsId) {
  return request.get('/favorite/check', { params: { news_Id: newsId } })
}

export function addFavorite(newsId) {
  return request.post('/favorite/add', { newsId })
}

export function removeFavorite(newsId) {
  return request.delete('/favorite/remove', { params: { news_Id: newsId } })
}

export function getFavoriteList(page = 1, pageSize = 10) {
  return request.get('/favorite/list', { params: { page, pageSize } })
}

export function clearFavorites() {
  return request.delete('/favorite/clear')
}
