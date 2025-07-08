# Отправка данных в Google Drive через DVC 
# (По идее работает, по факту google блокирует из-за защиты конфиденциальности)
import hydra, subprocess
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def dvc_push_to_gdrive(cfg: DictConfig) -> None:
    try:
        # Настройка удалённого хранилища (если ещё не сделано)
        subprocess.run(["dvc", "remote", "remove", cfg.PATH_DVC_TO_GDRIVE.remote_name], check=True)
        subprocess.run(["dvc", "remote", "add", "-d", cfg.PATH_DVC_TO_GDRIVE.remote_name,
                        f"gdrive://{cfg.PATH_DVC_TO_GDRIVE.gdrive_folder_id}"], check=True)

        # Отправка данных в Google Drive
        subprocess.run(["dvc", "push"], check=True)
        print("Данные успешно загружены в Google Drive через DVC.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    dvc_push_to_gdrive()