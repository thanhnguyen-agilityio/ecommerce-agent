# config.py

BASE_URL = "https://ivymoda.com/danh-muc/ao-nu"
# class name end with 'product'
CSS_SELECTOR="[class$='product']"
# class name start with 'product-detail'
PRODUCT_DETAIL_CSS_SELECTOR="[class^='product-detail']"
REQUIRED_PRODUCT_IN_LIST_KEYS = [
    "name",
    "url"
]
REQUIRED_PRODUCT_DETAIL_KEYS = [
    "name",
    "price",
    "quantity",
    "category",
    "description",
    "colors",
    "sizes",
    "thumbnail",
    "url",
]
NO_RESULT_MESSAGE = "Không tìm thấy sản phẩm phù hợp !"
ALLOW_COLOR = [
    *(f"{i:03}" for i in range(75))]  # '000' to '074'
ALLOW_SIZE = ["XS", "S", "M", "L", "XL", "XXL"]

