import pandas as pd
from sklearn.model_selection import train_test_split
import hydra
from omegaconf import DictConfig

@hydra.main(config_name="preprocessing-config", config_path="../../configs", version_base="1.1")
def preprocess_data(cfg: DictConfig) -> None:
    datairis = pd.read_csv(
        f"{cfg.PATH_TO_SAVE_CSV.input_dir}/{cfg.PATH_TO_SAVE_CSV.filename}", sep=',')

    y_iris = datairis['species']
    datairis = datairis.drop('species', axis=1)

    try:
        datairis = datairis.drop('Id', axis=1)
    except KeyError:
        pass

    datairis.columns[datairis.isna().any()].tolist()

    y_iris = y_iris.astype('category')

    codes = pd.Series(range(len(y_iris.cat.categories)), name='codes')
    classes = pd.Series(y_iris.cat.categories, name='class')
    class_names = pd.concat([codes, classes], axis=1)
    class_names.to_csv(
        f'{cfg.PATH_TO_SAVE_CSV.save_dir}/{cfg.PATH_TO_SAVE_CSV.class_names}',
        index=False)

    y_iris = y_iris.cat.codes

    data_train, data_test, answer_train, answer_test = train_test_split(datairis, y_iris, test_size=0.3)

    data_train.to_csv(f'{cfg.PATH_TO_SAVE_CSV.save_dir}/{cfg.PATH_TO_SAVE_CSV.data_train}', index=False, sep=',')
    data_test.to_csv(f'{cfg.PATH_TO_SAVE_CSV.save_dir}/{cfg.PATH_TO_SAVE_CSV.data_test}', index=False, sep=',')
    answer_train.to_csv(f'{cfg.PATH_TO_SAVE_CSV.save_dir}/{cfg.PATH_TO_SAVE_CSV.answer_train}', index=False, sep=',')
    answer_test.to_csv(f'{cfg.PATH_TO_SAVE_CSV.save_dir}/{cfg.PATH_TO_SAVE_CSV.answer_test}', index=False, sep=',')

if __name__ == "__main__":
    preprocess_data()