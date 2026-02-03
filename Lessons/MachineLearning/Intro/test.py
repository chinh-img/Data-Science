from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import fetch_california_housing  # dataset mẫu

# 1. Lấy dữ liệu ví dụ
data = fetch_california_housing()
X, y = data.data, data.target

# 2. Chia train / validation (80% - 20%)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Tạo model đơn giản
model = DecisionTreeRegressor(random_state=42)

# 4. Train trên tập train
model.fit(X_train, y_train)

# 5. Tính lỗi trên train và validation
pred_train = model.predict(X_train)
pred_val = model.predict(X_val)

mae_train = mean_absolute_error(y_train, pred_train)
mae_val = mean_absolute_error(y_val, pred_val)

print("MAE trên Train:", mae_train)
print("MAE trên Validation:", mae_val)
