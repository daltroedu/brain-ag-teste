from validate_docbr import CPF, CNPJ


def validate_cpf_cnpj(value):
    if value:
        cpf_cnpj = ''.join(filter(str.isdigit, value))
        if len(cpf_cnpj) == 11:
            return CPF().validate(cpf_cnpj)
        elif len(cpf_cnpj) == 14:
            return CNPJ().validate(cpf_cnpj)
    return False
