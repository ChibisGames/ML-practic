import os
import json
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import hydra
from omegaconf import DictConfig


@hydra.main(config_name="train-config", config_path="../../configs", version_base="1.1")
def train_model(cfg: DictConfig) -> None:
    # Загрузка данных (в данном примере используем встроенный набор данных Iris)
    X_train = pd.read_csv(
        f"{cfg.PATH_TO_LOAD_CSV.input_dir}/{cfg.PATH_TO_LOAD_CSV.X_train}", sep=',')
    y_train = pd.read_csv(
        f"{cfg.PATH_TO_LOAD_CSV.input_dir}/{cfg.PATH_TO_LOAD_CSV.y_train}", sep=',')
    X_test = pd.read_csv(
        f"{cfg.PATH_TO_LOAD_CSV.input_dir}/{cfg.PATH_TO_LOAD_CSV.X_test}", sep=',')
    y_test = pd.read_csv(
        f"{cfg.PATH_TO_LOAD_CSV.input_dir}/{cfg.PATH_TO_LOAD_CSV.y_test}", sep=',')
    target_names = pd.read_csv(
        f"{cfg.PATH_TO_LOAD_CSV.input_dir}/{cfg.PATH_TO_LOAD_CSV.class_names}", sep=',')

    y_train = y_train.squeeze()
    y_test = y_test.squeeze()

    # Создание и обучение модели случайного леса
    rf_model = RandomForestClassifier(
        n_estimators=cfg.model_params.n_estimators,  # Количество деревьев в лесу
        max_depth=cfg.model_params.max_depth,    # Максимальная глубина дерева
        min_samples_split=cfg.model_params.min_samples_split,  # Минимальное количество образцов для разделения узла
        random_state=cfg.model_params.random_state    # Для воспроизводимости результатов
    )

    # Обучение модели
    rf_model.fit(X_train, y_train)

    # Предсказание на тестовых данных
    y_pred = rf_model.predict(X_test)

    # Оценка качества модели
    accuracy = accuracy_score(y_test, y_pred)
    metrics = {
    'accuracy': accuracy,
    'classification_report': classification_report(y_test, y_pred, target_names=target_names, output_dict=True),
    "loss_history": 
    { 
        "train_loss": None,  # Список значений loss
        "test_loss": None    # Если есть
    },
    }
    if cfg.launch == "single":
        # Сохранение модели
        with open(
            f"{cfg.PATH_TO_SAVE_MODEL.output_dir}/{cfg.PATH_TO_SAVE_MODEL.modelname}{\
                cfg.PATH_TO_SAVE_MODEL.model_expansion}", 'wb') as f:
            pickle.dump({'model': rf_model, 'metrics': metrics}, f)

        # Сохранение метрик в JSON файл
        with open(
            f"{cfg.PATH_TO_SAVE_MODEL.output_dir}/{cfg.PATH_TO_SAVE_MODEL.metricsname}{\
                cfg.PATH_TO_SAVE_MODEL.metrics_expansion}", 'w') as f:
            json.dump(metrics, f, indent=4)
    elif cfg.launch == "multirun":
        # Сохранение модели и метрик для каждого запуска
        with open(
            f"{cfg.PATH_TO_SAVE_MODEL.output_dir}/{cfg.PATH_TO_SAVE_MODEL.modelname}_{\
                cfg.PATH_TO_SAVE_MODEL.date_cat}_{cfg.PATH_TO_SAVE_MODEL.time_cat}{\
                cfg.PATH_TO_SAVE_MODEL.model_expansion}", 'wb') as f:
            pickle.dump({'model': rf_model, 'metrics': metrics}, f)
        with open(
            f"{cfg.PATH_TO_SAVE_MODEL.output_dir}/{cfg.PATH_TO_SAVE_MODEL.metricsname}_{\
                cfg.PATH_TO_SAVE_MODEL.date_cat}_{cfg.PATH_TO_SAVE_MODEL.time_cat}{\
                cfg.PATH_TO_SAVE_MODEL.metrics_expansion}", 'w') as f:
            json.dump(metrics, f, indent=4)


# Функция для типа запуска обучения модели
@hydra.main(config_name="train-config", config_path="../../configs", version_base="1.1")
def train_launch(cfg: DictConfig) -> None:
    if cfg.launch == "single": # Запуск в режиме single
        train_model(cfg)
    elif cfg.launch == "multirun": # Запуск в режиме multirun (обучения на всех папках с данными)
        for date_cat in os.listdir(cfg.PATH_TO_LOAD_CSV.root_dir):
            for time_cat in os.listdir(os.path.join(cfg.PATH_TO_LOAD_CSV.root_dir, date_cat)):
                if os.path.isdir(os.path.join(cfg.PATH_TO_LOAD_CSV.root_dir, date_cat, time_cat)):
                    cfg.PATH_TO_LOAD_CSV.input_dir = os.path.join(cfg.PATH_TO_LOAD_CSV.root_dir, date_cat, time_cat)
                    cfg.PATH_TO_SAVE_MODEL.date_cat = date_cat
                    cfg.PATH_TO_SAVE_MODEL.time_cat = time_cat
                    train_model(cfg)
                

    
if __name__ == "__main__":
    train_launch()