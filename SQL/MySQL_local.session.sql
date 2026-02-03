-- Khởi tạo CSDL
DROP DATABASE IF EXISTS to3; -- Xóa CSDL to3 nếu đã tồn tại (tránh lỗi)
CREATE DATABASE to3; -- Tạo CSDL to3
USE to3; -- Chọn CSDL để thực hiện các lệnh

-- Tạo các bảng
CREATE TABLE hoc_sinh (  -- Bảng gốc
    so_bao_danh VARCHAR(20) PRIMARY KEY, -- SBD là khóa chính
    the_hoc_sinh VARCHAR(20) UNIQUE, -- thẻ hs là UNIQUE để tránh trùng
    ho_ten VARCHAR(100),
    lop VARCHAR(20)
);

CREATE TABLE diem_hoc_tap (
    id INT AUTO_INCREMENT PRIMARY KEY, -- id cho AUTO_INCREMENT để tự tăng theo số lượng hs
    so_bao_danh VARCHAR(20),
    diem_toan FLOAT, -- Vì các điểm có thể là số thập phân nên để FLOAT
    diem_van FLOAT,
    diem_tin FLOAT,
    diem_li FLOAT,
    diem_anh FLOAT,
    diem_su FLOAT,
    diem_hoa FLOAT,
    xep_loai VARCHAR(20),
    FOREIGN KEY (so_bao_danh) REFERENCES hoc_sinh(so_bao_danh) -- khóa ngoại, liên kết sang bảng hoc_sinh
        ON DELETE CASCADE -- khi xóa học sinh (ở bảng gốc) thì xóa luôn điểm học tập
);

CREATE TABLE hanh_kiem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    so_bao_danh VARCHAR(20),
    hanh_kiem VARCHAR(20),
    FOREIGN KEY (so_bao_danh) REFERENCES hoc_sinh(so_bao_danh)
        ON DELETE CASCADE -- khi xóa học sinh (ở bảng gốc) thì xóa luôn hạnh kiểm
);

-- Thêm học sinh
INSERT INTO hoc_sinh VALUES -- Mặc định thêm dữ liệu theo thứ tự biến: (so_bao_danh, the_hoc_sinh, ho_ten, lop)
    ('K11001', 'THS001', 'Hoàng Trọng Chính', '11B4'),
    ('K11002', 'THS002', 'Hàn Nghi Du', '11B4'),
    ('K11003', 'THS003', 'Lê Trung Dũng', '11B4'),
    ('K11004', 'THS004', 'Đỗ Quốc Huy', '11B4'),
    ('K11005', 'THS005', 'Phạm Minh Khoa', '11B4'),
    ('K11006', 'THS006', 'Nguyễn Lâm Tuấn Kiệt', '11B4'),
    ('K11007', 'THS007', 'Võ Xuân Ngân', '11B4'),
    ('K11008', 'THS008', 'Đoàn Bá Nhật', '11B4'),
    ('K11009', 'THS009', 'Nguyễn Nam Phát', '11B4'),
    ('K11010', 'THS010', 'Võ Thị Thanh Phương', '11B4'),
    ('K11011', 'THS011', 'Lê Hoàng Tú Uyên', '11B4'),
    ('K11012', 'THS012', 'Phạm Quang Vinh', '11B4'),
    ('K11013', 'THS013', 'A', '11B4');

-- Thêm điểm
INSERT INTO diem_hoc_tap (so_bao_danh, diem_toan, diem_van, diem_tin, diem_li, diem_anh, diem_su, diem_hoa, xep_loai) VALUES
    -- Các giá trị chèn theo đúng thứ tự các biến trong ds dữ liệu chèn
    ('K11001', 9.8, 7.5, 10, 7, 8 ,8.3, 9, 'Giỏi'),
    ('K11002', 8, 8.8, 9, 7, 9 ,8.5, 9.5, 'Giỏi'),
    ('K11003', 8, 7.8, 9, 7, 9.2 ,8.5, 9.5, 'Giỏi'),
    ('K11004', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11005', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11006', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11007', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11008', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11009', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11010', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi'),
    ('K11011', 8.3, 9, 9.5, 8.8, 10 ,8.5, 9.8, 'Giỏi'),
    ('K11012', 8, 7, 9, 7, 8.9 ,8.5, 8, 'Giỏi');

-- Thêm hạnh kiểm
INSERT INTO hanh_kiem (so_bao_danh, hanh_kiem) VALUES
    ('K11001', 'Tốt'),
    ('K11002', 'Tốt'),
    ('K11003', 'Tốt'),
    ('K11004', 'Tốt'),
    ('K11005', 'Tốt'),
    ('K11006', 'Tốt'),
    ('K11007', 'Tốt'),
    ('K11008', 'Tốt'),
    ('K11009', 'Tốt'),
    ('K11010', 'Tốt'),
    ('K11011', 'Tốt'),
    ('K11012', 'Tốt');

-- Xem dữ liệu
SELECT hs.so_bao_danh, hs.the_hoc_sinh, hs.ho_ten, hs.lop,
       d.diem_toan, d.diem_van, d.diem_tin, d.diem_li, d.diem_anh,d.diem_su, d.diem_hoa,
       d.xep_loai, hk.hanh_kiem
    FROM hoc_sinh hs
    JOIN diem_hoc_tap d ON hs.so_bao_danh = d.so_bao_danh -- Nối dữ liệu bằng trường giống nhau giữa các bảng (SBD)
    JOIN hanh_kiem hk ON hs.so_bao_danh = hk.so_bao_danh;

-- Sửa dữ liệu
UPDATE diem_hoc_tap
    SET diem_toan = 7, diem_van = 7, diem_tin = 10, diem_su = 9, diem_hoa = 9.3, xep_loai = 'Giỏi'
    WHERE so_bao_danh = 'K11001';

-- Xóa dữ liệu
DELETE FROM hoc_sinh WHERE the_hoc_sinh = 'THS013'; -- Xóa học sinh có thẻ hs là THS013