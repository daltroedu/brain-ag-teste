from localflavor.br.validators import BRCPFValidator, BRCNPJValidator


def validate_cpf_cnpj(value):
    cpf_cnpj = ''.join(filter(str.isdigit, value))
    try:
        if len(cpf_cnpj) == 11:
            BRCPFValidator()(cpf_cnpj)
        elif len(cpf_cnpj) == 14:
            BRCNPJValidator()(cpf_cnpj)
        else:
            return False
    except ValueError:
        return False
    return True
