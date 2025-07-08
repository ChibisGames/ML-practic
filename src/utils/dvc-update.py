import hydra, subprocess
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def dvc_update(cfg: DictConfig) -> None:
    for int_file in cfg.PATH_TO_DVC.internal_files:
        try:
            subprocess.run(["dvc", "update", f"{int_file}"], 
                           cwd=cfg.PATH_TO_DVC.target_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при обновлении DVC для {int_file}: {e}")

if __name__ == "__main__":
    dvc_update()