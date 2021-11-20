# Recommendation System

- 
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
python rating.py
python genre.py
python movies.py
```
Sau đó chúng ta sẽ thu được các file sau:
```sh
list_genres.json   # Dùng để lưu lại các thể loại của phim
movies.json        # Dùng để lưu các thông tin và url của phim
neighbors.npy      # File numpy sau khi đã sắp xếp các bộ phim có cùng thể loại
rating.npy         # File numpy sau khi đã sắp xếp lượt đánh giá gần bằng nhau
```
Tiếp tục duy chuyển các file vừa thu được vào thư mục Website
Trên windows:
```sh
move ./list_genres.json ../Website/data
move ./movies.json ../Website/data
move ./neighbors.npy ../Website/data
move ./rating.npy ../Website/data
```
Trên linux:
```sh
mv ./list_genres.json ../Website/data
mv ./movies.json ../Website/data
mv ./neighbors.npy ../Website/data
mv ./rating.npy ../Website/data
```
### Chạy chương trình
```sh
cd ../Website
set FLASK_APP=main.py
flask run
```
