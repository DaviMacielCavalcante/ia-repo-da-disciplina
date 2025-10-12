import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


def fuzzy_config(show_pertinencia=False):
    # Variáveis fuzzy
    clima = ctrl.Antecedent(np.arange(0, 11, 1), "clima")
    qualidade_estrada = ctrl.Antecedent(np.arange(0, 11, 1), "qualidade_estrada")
    mult = ctrl.Consequent(np.arange(0.5, 3.1, 0.1), "mult")

    # Funções de pertinência
    clima["ruim"] = fuzz.gaussmf(clima.universe, 0, 1.5)
    clima["moderado"] = fuzz.gaussmf(clima.universe, 5, 1.5)
    clima["bom"] = fuzz.gaussmf(clima.universe, 10, 1.5)

    qualidade_estrada["pessima"] = fuzz.trimf(qualidade_estrada.universe, [0, 0, 2.5])
    qualidade_estrada["ruim"] = fuzz.gaussmf(qualidade_estrada.universe, 3.5, 1.2)
    qualidade_estrada["regular"] = fuzz.gaussmf(qualidade_estrada.universe, 6, 1.2)
    qualidade_estrada["boa"] = fuzz.trimf(qualidade_estrada.universe, [7.5, 10, 10])

    mult["ideal"] = fuzz.trapmf(mult.universe, [0.5, 0.5, 0.7, 0.8])
    mult["baixo"] = fuzz.trapmf(mult.universe, [0.7, 0.9, 1.0, 1.2])
    mult["medio"] = fuzz.trapmf(mult.universe, [1.0, 1.2, 1.4, 1.6])
    mult["alto"] = fuzz.trapmf(mult.universe, [1.4, 1.7, 2.1, 2.5])
    mult["altissimo"] = fuzz.trapmf(mult.universe, [2.3, 2.7, 3.0, 3.0])

    if show_pertinencia:
        clima.view()
        qualidade_estrada.view()
        mult.view()
        plt.show()

    # Clima ruim
    regra1 = ctrl.Rule(clima["ruim"] & qualidade_estrada["pessima"], mult["altissimo"])
    regra2 = ctrl.Rule(clima["ruim"] & qualidade_estrada["ruim"], mult["alto"])
    regra3 = ctrl.Rule(clima["ruim"] & qualidade_estrada["regular"], mult["alto"])
    regra4 = ctrl.Rule(clima["ruim"] & qualidade_estrada["boa"], mult["baixo"])

    # Clima moderado
    regra5 = ctrl.Rule(clima["moderado"] & qualidade_estrada["pessima"], mult["alto"])
    regra6 = ctrl.Rule(clima["moderado"] & qualidade_estrada["ruim"], mult["alto"])
    regra7 = ctrl.Rule(clima["moderado"] & qualidade_estrada["regular"], mult["medio"])
    regra8 = ctrl.Rule(clima["moderado"] & qualidade_estrada["boa"], mult["baixo"])

    # Clima bom
    regra9 = ctrl.Rule(clima["bom"] & qualidade_estrada["pessima"], mult["alto"])
    regra10 = ctrl.Rule(clima["bom"] & qualidade_estrada["ruim"], mult["baixo"])
    regra11 = ctrl.Rule(clima["bom"] & qualidade_estrada["regular"], mult["baixo"])
    regra12 = ctrl.Rule(clima["bom"] & qualidade_estrada["boa"], mult["ideal"])

    return [
        regra1,
        regra2,
        regra3,
        regra4,
        regra5,
        regra6,
        regra7,
        regra8,
        regra9,
        regra10,
        regra11,
        regra12,
    ]


# Para ver os gráficos das funções de pertinência:
# fuzzy_config(show_pertinencia=True)

# TESTES:

sistema_fuzzy = ctrl.ControlSystem(fuzzy_config())
simulador = ctrl.ControlSystemSimulation(sistema_fuzzy)

print("=== VALORES DE TESTE DA LÓGICA ===")

casos_teste = [
    (0, 0, "Pior caso"),  # clima ruim + estrada péssima
    (10, 10, "Melhor caso"),  # clima bom + estrada boa
    (0, 10, "Clima ruim, estrada boa"),
    (10, 0, "Clima bom, estrada péssima"),
    (5, 5, "Tudo médio"),
]

for clima_val, estrada_val, descricao in casos_teste:
    simulador.input["clima"] = clima_val
    simulador.input["qualidade_estrada"] = estrada_val
    simulador.compute()
    print(f"{descricao}: mult = {simulador.output['mult']:.2f}")
    
print("=== FIM DOS TESTES ===\n")
