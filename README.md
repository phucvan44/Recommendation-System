# Recommendation System

### Tổng quang về Recommendation System
- Recommend dựa trên đánh giá của người dùng
- Recommend dựa trên thể loại của phim

#### Recommend dựa trên đánh giá của người dùng
Tính trung bình cộng các lượt đánh giá của người dùng từ 0.0 đến 5.0. Sắp xếp các bộ phim có trung bình cộng các lượt đánh giá gần bằng bộ phim mà người dùng đang xem.
#### Recommend dựa trên thể loại của phim
Lọc ra các thể loại của phim. Sắp xếp các bộ phim có cùng nhiều thể loại với bộ phim đang xem nhất

# Thực hiện
### Yêu cầu thư viện trong Python
- numpy
- pandas
- json
- flask


### Tiền xử lý dữ liệu
Chúng ta cần tiền xử lý dữ liệu để khi dùng chỉ ta chỉ cần import các module cần thiết và không cần phải mất thời gian train lại model.

Mở thư mục hiện tại và làm các bước sau

```sh
cd clearn_data
python main.py
```
Sau đó chúng ta sẽ thu được các file sau:
```sh
genres_contents.json   # Dùng để lưu lại các thể loại của phim
genres_neighbors.npy   # Dùng để lưu các bộ phim có cùng các thể loại
movies_contents.json   # Dùng để lưu lại thông tin các bộ phim
rating_neighbors.npy   # Dùng để lưu các bộ phim có các lượt đánh giá gần bằng nhau
```
Tiếp tục duy chuyển các file vừa thu được vào thư mục Website
Trên windows:
```sh
move ./genres_contents.json ../Website/data
move ./genres_neighbors.npy ../Website/data
move ./movies_contents.json ../Website/data
move ./rating_neighbors.npy ../Website/data
```
Trên linux:
```sh
mv ./genres_contents.json ../Website/data
mv ./genres_neighbors.npy ../Website/data
mv ./movies_contents.json ../Website/data
mv ./rating_neighbors.npy ../Website/data
```
### Chạy chương trình
```sh
cd ../Website
set FLASK_APP=main.py
flask run
```
