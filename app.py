import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Food Calorie Classifier",
    page_icon="🍽️",
    layout="centered"
)

MODEL_PATH = "models/mobilenet_food_classifier.h5"

CLASS_NAMES = {
    0: "Burger",
    1: "Cake",
    2: "French Fries",
    3: "Ice Cream",
    4: "Paneer Dish",
    5: "Pasta",
    6: "Pizza",
    7: "Salad",
    8: "Sandwich"
}

CALORIE_MAP = {
    "Burger": "250–300 kcal",
    "Cake": "300–350 kcal",
    "French Fries": "300–365 kcal",
    "Ice Cream": "200–250 kcal",
    "Paneer Dish": "300–400 kcal",
    "Pasta": "350–400 kcal",
    "Pizza": "250–300 kcal (per slice)",
    "Salad": "120–180 kcal",
    "Sandwich": "250–300 kcal"
}

# ------------------ LOAD MODEL ------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

# ------------------ FUNCTIONS ------------------
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# ------------------ UI ------------------
st.title("🍽️ Food Calorie Image Classifier")
st.caption("Deep Learning (MobileNetV2 + Transfer Learning)")
st.write("Upload a food image to identify the food item and estimate its calorie range.")

uploaded_file = st.file_uploader(
    "Upload a food image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)[0]

    top_idx = np.argmax(predictions)
    confidence = predictions[top_idx]

    food_name = CLASS_NAMES[top_idx]
    calories = CALORIE_MAP[food_name]

    st.divider()
    st.subheader("🔍 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Food Item", food_name)

    with col2:
        st.metric("Estimated Calories", calories)

    st.write("### 🔐 Confidence Level")
    st.progress(float(confidence))
    st.write(f"**{confidence * 100:.2f}% confident**")

    # ------------------ TOP-3 PREDICTIONS ------------------
    st.write("### 📊 Top Predictions")

    top_3 = predictions.argsort()[-3:][::-1]

    for idx in top_3:
        st.write(
            f"**{CLASS_NAMES[idx]}** — {predictions[idx] * 100:.2f}%"
        )

    st.caption(
        "⚠️ Calorie values are approximate and depend on portion size."
    )
