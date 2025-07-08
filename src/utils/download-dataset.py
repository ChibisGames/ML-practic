# Данный файл используем, если можно скачать датасет из интернета, 
# то есть он не подвязан к удалённому хранилищу.
import hydra, os, urllib.request
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def download_dataset(cfg: DictConfig) -> None:

    # Настройки
    os.makedirs(cfg.PATH_TO_DOWNLOAD_FROM_INTERNET.output_dir, exist_ok=True)
    output_path = os.path.join(cfg.PATH_TO_DOWNLOAD_FROM_INTERNET.output_dir,
                               cfg.PATH_TO_DOWNLOAD_FROM_INTERNET.filename)

    # Загрузка файла
    urllib.request.urlretrieve(cfg.PATH_TO_DOWNLOAD_FROM_INTERNET.url, output_path)
    print(f"Файл загружен: {output_path}")


if __name__ == "__main__":
    download_dataset()