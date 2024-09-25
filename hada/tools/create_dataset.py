# TODO
# classificar o andamento usando o lamma3.1 e permitir editar o resultado jogando num arquivo para usar como base de dados.
import os
import ast
import torch
import transformers
from tqdm import tqdm

from hada.consts import PROMPT_PATH, CURR_PATH
from hada.utils import DATA


DATASET_PATH = os.path.join(CURR_PATH, "hada/data/LAW_PROG_classify.csv")


CLASSES = {
    0: "sem_merito",
    1: "procedente",
    2: "improcedente",
    3: "parcialmente_procedente",
    4: "homologado",
    5: "extincao_do_processo",
    6: "nao_classificado",
}


def load_prompt_file():
    return open(PROMPT_PATH, "r").read()


def open_dataset_csv():
    dataset_file = open(DATASET_PATH, "r+")
    dataset = dataset_file.readlines()

    if len(dataset) < 1:
        dataset_file.write("lawsuit_id;content;sentence\n")

    return dataset_file, dataset


class LammaModelHuggingFace:
    def __init__(self) -> None:
        self.model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

    def _parse_response(self, output):
        res = {"Classificação": ""}
        try:
            res = ast.literal_eval(output[0]["generated_text"][-1]["content"])
        except:
            pass
        return res

    def infer(self, messages):
        return self._parse_response(
            self.pipeline(
                messages,
                max_new_tokens=256,
            )
        )


def main():
    lines = load_prompt_file()
    lamma_model = LammaModelHuggingFace()
    dataset_file, dataset = open_dataset_csv()
    lawsuit_ids = [law_id.split(";")[0] for law_id in dataset]

    for lawsuit_id, lawsuits in tqdm(DATA.items(), position=0):
        for i, lawsuit in tqdm(enumerate(lawsuits), position=1):
            if f"{lawsuit_id}__{i}__" in lawsuit_ids:
                print(f"SKIPPING: {lawsuit_id}__{i}")
                continue

            if lawsuit["Classificacao"][0] != "procedente":
                continue

            if len(lawsuit["Conteudo"]) > 6000:
                continue

            LAWSUIT_LINE = {}
            messages = [
                {
                    "role": "system",
                    "content": f"Você será apresentado a andamentos de processos públicos e seu trabalho é gerar um JSON como os exemplos abaixo. Sua resposta será apenas um JSON contendo as informações pedidas. Para o campo de 'Classificação' ESCOLHA APENAS UMA tag dentre 'sem_merito', 'parcialmente_procedente', 'procedente', 'improcedente', 'homologado', 'extincao_do_processo' e 'nao_classificado' (escolha apenas uma, NUNCA duas ou mais). USE O EXEMPLO ABAIXO COMO RESULTADO DO JSON ESPERADO:\n    \n{lines}",
                },
                {
                    "role": "user",
                    "content": lawsuit["Conteudo"],
                },
            ]

            LAWSUIT_LINE["lawsuit_id"] = f"{lawsuit_id}__{i}__"
            LAWSUIT_LINE["content"] = lawsuit["Conteudo"]

            res = lamma_model.infer(messages)
            print("_" * 50)
            print(f"\nContent:\n\n{lawsuit['Conteudo']}\n\n")
            print(f"{lamma_model.model_id} predicted class: {res}\n")
            print("_" * 50)

            user_resp = int(
                input("\nuse lamma model predicted_class: \n1- yes\n2- no\n9- stop\n")
            )

            if user_resp == 1:
                LAWSUIT_LINE["sentence"] = res["Classificação"]

            if user_resp == 2:
                pretty_str = "".join([f"{k} - {v}\n" for k, v in CLASSES.items()])
                user_sentence = int(input(f"input the real sentence:\n{pretty_str}"))
                LAWSUIT_LINE["sentence"] = CLASSES.get(user_sentence)

            if user_resp == 9:
                dataset_file.close()
                return

            write_line = ";".join([v for v in LAWSUIT_LINE.values()])
            dataset_file.write(f"{write_line}\n")


if __name__ == "__main__":
    main()
