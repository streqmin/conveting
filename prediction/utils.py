import os
import numpy as np
from keras.api.models import load_model
from keras.api.preprocessing.image import img_to_array

# 질환명 ↔ 코드 매핑
eye_diseases = {
    "conjunctivitis": "E1",
    "corneal_ulcer": "E2",
    "cataract": "E3",
    "nonulcer_keratitis": "E4",
    "nonulcer_keratitis": "E5",
    "entropion": "E6",
    "안검염": "E7",
    "eyelid_tumor": "E8",
    "epiphora": "E9",
    "핵경화": "E10",
}

skin_diseases = {
    "papule_plaque": "A1",
    "scale_collarette": "A2",
    "lichen_hyperpig": "A3",
    "pustule_acne": "A4",
    "erosion_ulcer": "A5",
    "nodule_mass": "A6",
}


def load_models_from_dir(disease_map, model_dir, prefix_length=2):
    """
    disease_map: {"질환명": "모델코드"} 형태
    model_dir: 실제 모델 파일들이 저장된 디렉토리 경로
    prefix_length: 모델코드 길이 (예: 'E0', 'A3' → 2글자)
    """
    models = {}

    for filename in os.listdir(model_dir):
        if not filename.endswith(".keras"):
            continue

        # 파일명에서 코드 추출
        code = filename.split("_")[0]
        model_path = os.path.join(model_dir, filename)

        for disease, expected_code in disease_map.items():
            if expected_code == code and disease not in models:
                models[disease] = load_model(model_path)
                break  # 중복 로딩 방지

    # 누락된 항목 확인
    for disease in disease_map:
        if disease not in models:
            print(f"[경고] '{disease}'에 해당하는 모델 파일을 찾을 수 없습니다.")

    return models


# 실제 모델 로딩
eye_models = load_models_from_dir(eye_diseases, "./ai_weights/eye")
skin_models = load_models_from_dir(skin_diseases, "./ai_weights/skin")


def preprocess_image(img, target_size):
    """이미지를 Keras 모델에 맞게 전처리하는 함수"""
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # 이미지 정규화
    return img_array


def predict_diseases(img, model_dict):
    """질환 모델 딕셔너리를 기반으로 전체 확률 예측"""
    results = {}
    target_size = (224, 224)
    img_array = preprocess_image(img, target_size)

    probabilities = []
    for disease, model in model_dict.items():
        prediction = model.predict(img_array)
        probability = prediction[0][0]
        probabilities.append(probability)
        results[disease] = probability

    total_probability = sum(probabilities)
    normalized_results = {
        disease: (prob / total_probability) * 100 for disease, prob in results.items()
    }

    return normalized_results


def predict_eye_diseases(img, eye_models):
    """안구 질환 중 확률이 높은 Top-2만 반환"""
    full_results = predict_diseases(img, eye_models)
    top2 = sorted(full_results.items(), key=lambda x: x[1], reverse=True)[:2]
    return dict(top2)


def predict_skin_diseases(img, skin_models):
    """피부 질환 중 확률이 높은 Top-2만 반환"""
    full_results = predict_diseases(img, skin_models)
    top2 = sorted(full_results.items(), key=lambda x: x[1], reverse=True)[:2]
    return dict(top2)



def run_diagnosis(image_path, diagnosis_part):
    """진단 부위에 따라 적절한 예측 함수를 호출하는 메인 함수"""
    if diagnosis_part == "eye":
        return predict_eye_diseases(image_path)
    elif diagnosis_part == "skin":
        return predict_skin_diseases(image_path)
    else:
        raise ValueError("Invalid diagnosis part. Choose 'eye' or 'skin'.")
