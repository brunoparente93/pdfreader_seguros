import pdfplumber
import pandas as pd
import streamlit as st

# Streamlit UI

# carro = st.text_input("Nome do veículo")
# st.write("Nome do veiculo é: ", carro)
option1 = st.selectbox(
    "Selecione a seguradora atual",
    ('00',"01", "02", "03","04", "05", "06","07", "08", "09","10", "11", "12"))
option = st.selectbox(
    "Selecione a seguradora com a melhor opcao",
    ('00',"01", "02", "03","04", "05", "06","07", "08", "09","10", "11", "12"))

if option1==option:
    st.warning('Seguradora atual igual seguradora com melhor opcao!', icon="⚠️")

pdf_file = st.file_uploader('Choose your .pdf file', type="pdf")



if pdf_file is not None:
    parameters = ['APP', 'Assistência 24 Horas', 'Valor do seguro', 'Carro Reserva',
                  'Fipe', 'Retrovisores/Faróis/Lanternas', 'Cobertura de Vidros', 'Franquia',
                  'RCF - Danos Materiais', 'RCF - Danos Corporais', 'RCF - Danos Morais']
    data = {key: [] for key in parameters}

    # Open and read the uploaded PDF file
    with pdfplumber.open(pdf_file) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.split('\n'))

    if lines:
        indexes_list = []
        # Loop through each line and search for the pattern
        for index, item in enumerate(lines):
            if item.startswith('R$'):
                initial_index = index - 1
                indexes_list.append(initial_index)

        if indexes_list:
            index_initial = indexes_list[0]
            # st.text(index_initial)
            # st.text(lines[index_initial])

            # Process each line once, and extract all required fields
            for item in lines:
                if "APP:" in item:
                    result_app = item.split("APP:")[1]
                    result_app = result_app.replace('Selecione...', 'R$ 0,00').strip()
                    result_app = result_app.split('R$')[1:]

                    result_app2 = list(lines[index_initial + 7])  # This converts the 7th element of 'lines' into a list
                    # Assuming you want to split a string inside the list, you should access that string first

                    # For example, if 'lines[index_initial + 7]' is a single string:
                    result_app2 = lines[index_initial + 7].replace('Selecione...', 'R$ 0,00').strip()  # Access the string directly
                    result_app2 = result_app2.split('R$')[1:]  # Now apply the split on the string

                    data['APP'] = result_app+result_app2

                # Extract "Assistência 24 Horas:" information
                elif "Assistência 24 Horas:" in item:
                    result_assistencia = item.split("Assistência 24 Horas:")[1]
                    result_assistencia = (result_assistencia
                                        .replace('Km Ilimitada', '10000 KM')
                                        .replace('Plano M', '10000 KM')
                                        .replace('km', 'KM').replace('Km', 'KM').strip())
                    result_assistencia = result_assistencia.split('KM')[:-1]
                    result_assistencia = [i.strip() for i in result_assistencia]
                    result_assistencia = ['ilimitado' if i == '10000' or i == 'Plano M' else i for i in result_assistencia]

                    result_assistencia2=  lines[index_initial + 8]
                    result_assistencia2= (result_assistencia2
                                        .replace('Km Ilimitada', '10000 KM')
                                        .replace('km', 'KM').replace('Km', 'KM').strip())
                    result_assistencia2 = result_assistencia2.split('KM')[:-1]
                    result_assistencia2 = [i.strip() for i in result_assistencia2]
                    result_assistencia2 = ['ilimitado' if i == '10000' or i == 'Plano M' else i for i in result_assistencia2]

                    data['Assistência 24 Horas'] = result_assistencia + result_assistencia2

                # Extract "Cobertura de Vidros:" information
                elif "Cobertura de Vidros: " in item:
                    result_vidros = item.split("Cobertura de Vidros: ")[1]
                    result_vidros = result_vidros.split(' ')[1:]

                    result_vidros2= lines[index_initial + 9]
                    result_vidros2 = item.split("Cobertura de Vidros: ")[1]
                    result_vidros2 = result_vidros2.split(' ')

                    data['Cobertura de Vidros'] = result_vidros+result_vidros2

                # Extract "Retrovisores/Faróis/Lanternas:" information
                elif "Retrovisores/Faróis/Lanternas:" in item:
                    result_retrovisores = item.split("Retrovisores/Faróis/Lanternas:")[1]
                    result_retrovisores = result_retrovisores.split(' ')[1:]

                    result_retrovisores2=lines[index_initial + 10]
                    result_retrovisores2 = result_retrovisores2.split(' ')#[1:]

                    data['Retrovisores/Faróis/Lanternas'] = result_retrovisores +result_retrovisores2

                # Extract "% Fipe:" information
                elif "% Fipe: " in item:
                    result_fipe = item.split("% Fipe: ")[1]
                    result_fipe = result_fipe.replace(' ', '').split('%')[:-1]

                    result_fipe2=lines[index_initial + 2]
                    result_fipe2=result_fipe2.replace(' ', '').split('%')[:-1]

                    data['Fipe'] = result_fipe+result_fipe2

                # Extract "Carro Reserva:" information
                elif item.startswith('Carro Reserva:'):
                    result_reserva = item.split("Carro Reserva:")[1].strip().split('AR')[:-1]
                    result_reserva = [i.strip() for i in result_reserva]

                    result_reserva2=lines[index_initial+11]
                    result_reserva2= result_reserva2.strip().split('AR')[:-1]
                    result_reserva2 = [i.strip() for i in result_reserva2]


                    data['Carro Reserva'] = result_reserva+result_reserva2

                # Extract "Carro Reserva:" information
                elif item.startswith('Forma de Pagamento:'):
                    result_pagamento = item.split("Forma de Pagamento:")[1]
                    result_pagamento= result_pagamento.split(' ')
                    result_pagamento= [i for i in result_pagamento if i in ['Cartão','Carnê']]

                    result_pagamento2=lines[index_initial + 12]
                    result_pagamento2= result_pagamento2.split(' ')
                    result_pagamento2= [i for i in result_pagamento2 if i in ['Cartão','Carnê']]

                    data['Forma de Pagamento'] = result_pagamento+result_pagamento2

                # Extract "Valor do seguro"
                elif item.startswith('Valor do seguro'):
                    result_valor_seguro = item.split('Valor do seguro')
                    result_valor_seguro = result_valor_seguro[1].split('R$')
                    result_valor_seguro = result_valor_seguro[1:]
                    result_valor_seguro = [i.strip() for i in result_valor_seguro]

                    result_valor_seguro2=lines[index_initial + 1]
                    result_valor_seguro2 = result_valor_seguro2.split('R$')
                    result_valor_seguro2 = result_valor_seguro2[1:]
                    result_valor_seguro2 = [i.strip() for i in result_valor_seguro2]


                    data['Valor do seguro'] = result_valor_seguro+result_valor_seguro2

                # Extract "Franquia"
                elif item.startswith('Franquia'):
                    result_franquia = item.split('Franquia')
                    result_franquia = result_franquia[1].split('R$')
                    result_franquia = result_franquia[1:]
                    result_franquia = [i.strip() for i in result_franquia]

                    result_franquia2=lines[index_initial+3]
                    result_franquia2 = result_franquia2.split('R$')
                    result_franquia2 = result_franquia2[1:]
                    result_franquia2 = [i.strip() for i in result_franquia2]

                    data['Franquia'] = result_franquia+result_franquia2

                # Extract "RCF - Danos Materiais"
                elif item.startswith('RCF - Danos Materiais'):
                    result_rcf_materiais = item.split('RCF - Danos Materiais')
                    result_rcf_materiais = result_rcf_materiais[1].split('R$')
                    result_rcf_materiais = result_rcf_materiais[1:]
                    result_rcf_materiais = [i.strip() for i in result_rcf_materiais]

                    result_rcf_materiais2=lines[index_initial+4]
                    result_rcf_materiais2 = result_rcf_materiais2.split('R$')
                    result_rcf_materiais2 = result_rcf_materiais2[1:]
                    result_rcf_materiais2 = [i.strip() for i in result_rcf_materiais2]


                    data['RCF - Danos Materiais'] = result_rcf_materiais + result_rcf_materiais2

                # Extract "RCF - Danos Corporais"
                elif item.startswith('RCF - Danos Corporais'):
                    result_rcf_corporais = item.split('RCF - Danos Corporais')
                    result_rcf_corporais = result_rcf_corporais[1].split('R$')
                    result_rcf_corporais = result_rcf_corporais[1:]
                    result_rcf_corporais = [i.strip() for i in result_rcf_corporais]

                    result_rcf_corporais2=lines[index_initial+5]
                    result_rcf_corporais2 = result_rcf_corporais2.split('R$')
                    result_rcf_corporais2 = result_rcf_corporais2[1:]
                    result_rcf_corporais2 = [i.strip() for i in result_rcf_corporais2]


                    data['RCF - Danos Corporais'] = result_rcf_corporais + result_rcf_corporais2

                # Extract "RCF - Danos Morais"
                elif item.startswith('RCF - Danos Morais'):
                    result_rcf_morais = item.split('RCF - Danos Morais')
                    result_rcf_morais = result_rcf_morais[1].split('R$')
                    result_rcf_morais = result_rcf_morais[1:]
                    result_rcf_morais = [i.strip() for i in result_rcf_morais]

                    result_rcf_morais2=lines[index_initial+6]
                    result_rcf_morais2 = result_rcf_morais2.split('R$')
                    result_rcf_morais2 = result_rcf_morais2[1:]
                    result_rcf_morais2 = [i.strip() for i in result_rcf_morais2]

                    data['RCF - Danos Morais'] = result_rcf_morais + result_rcf_morais2

            
                elif item.startswith('Item:'):
                    veiculo = item.split('Item:')
                
                elif item.startswith('Proponente:'):
                    nome_cliente= item.split('Proponente:')




                
            # for i in data.keys():
            #     st.text(f'{i}: {len(data[i])}')
            # Create DataFrame and apply formatting
            df = pd.DataFrame(data)
            for i in df.columns:
                if i in ['APP', 'Valor do seguro', 'Franquia', 'RCF - Danos Materiais', 'RCF - Danos Corporais', 'RCF - Danos Morais']:
                    df[i] = df[i].apply(lambda x: 'R$ ' + x)
                if i == 'Assistência 24 Horas':
                    df[i] = df[i].apply(lambda x: x + ' km' if x != 'ilimitado' else x)
                if i == 'Carro Reserva':
                    df[i] = df[i].apply(lambda x: x + ' ar')
                if i == 'Fipe':
                    df[i] = df[i].apply(lambda x: x + '%')
            
            df = df[['APP', 'Assistência 24 Horas',  'Carro Reserva',
                'Fipe', 'Retrovisores/Faróis/Lanternas', 'Cobertura de Vidros',
                'RCF - Danos Materiais', 'RCF - Danos Corporais',
                'RCF - Danos Morais', 'Forma de Pagamento', 'Franquia', 'Valor do seguro']]


            df.rename(columns={'APP':'Acidentes pessoais de passageiros'}, inplace=True)
            option_selected=int(option)
            melhor_opcao = df.loc[[option_selected]] 
            melhor_opcao.drop(columns='Forma de Pagamento',inplace=True)

            option_selected_atual=int(option1)
            atual_opcao = df.loc[[option_selected_atual]] 
            seguradora_atual = df.loc[[option_selected_atual]] 
            seguradora_atual.drop(columns='Forma de Pagamento',inplace=True)
            # st.dataframe(seguradora_atual)

            df.drop(index=option_selected,inplace=True)
            
            df=df[['Valor do seguro','Franquia']]
           # st.dataframe(df)


            # Assuming df is your DataFrame
            # for index, row in df.iterrows():

            #     valorSeguro=float(row[2][3:].replace('.', '').replace(',', '.'))
            #     seguradora= f'SEGURADORA {index}'+'\n'
            #     result = seguradora+'\n'.join([f'{col}: {row[col]}' for col in df.columns])
            #     st.text(result)

            #     st.text('\n'+'Pagamento parcelado:')
                # for i in range(1,7):
                #     st.text(f'{i} x R$ {round(valorSeguro/i,2)}')




            #     st.text('__________________________')
            all_output_atual = ''

            for index, row in seguradora_atual.iterrows():
                
                # Convert the "Valor do seguro" column to a float by removing 'R$', and replacing the comma
                textoInicial= f'''Bom dia{nome_cliente[1]},\n\nO seguro do seu veículo está vencendo. Segue a melhor condição para a renovação da sua apólice.\n\n'''
                valorSeguro = float(row[-1][3:].replace('.', '').replace(',', '.'))
                seguradora = f'Veículo - {veiculo[1]}\n\nCOBERTURAS SEGURADORA {index} ATUAL:\n'

                # Create the result string for the current row
                result =textoInicial+ seguradora + '\n'.join([f'{col}: {row[col]}' for col in seguradora_atual.columns])

                # Add to all_output
                all_output_atual += result + '\n'
                all_output_atual += '\n' + 'Pagamento parcelado:\n'

                # Add parcel information
                for i in range(1, 7):
                    # Correct the round function usage
                    valor_parcela = round(valorSeguro / i, 2)
                    valor_parcela_str = str(valor_parcela).replace('.', ',')
                    
                    all_output_atual += f'{i} x R$ {valor_parcela_str}\n'

            all_output = ''

            for index, row in melhor_opcao.iterrows():
                
                # Convert the "Valor do seguro" column to a float by removing 'R$', and replacing the comma
                # textoInicial= f'''Bom dia{nome_cliente[1]},\n\nO seguro do seu veículo está vencendo. Segue a melhor condição para a renovação da sua apólice.\n\n'''
                valorSeguro = float(row[-1][3:].replace('.', '').replace(',', '.'))
                seguradora = f'\nCOBERTURAS DA SEGURADORA {index} COM A MELHOR CONDICAO:\n'

                # Create the result string for the current row
                result = seguradora+'\n'.join([f'{col}: {row[col]}' for col in melhor_opcao.columns])

                # Add to all_output
                all_output += result + '\n'
                all_output += '\n' + 'Pagamento parcelado:\n'

                # Add parcel information
                for i in range(1, 7):
                    # Correct the round function usage
                    valor_parcela = round(valorSeguro / i, 2)
                    valor_parcela_str = str(valor_parcela).replace('.', ',')
                    
                    all_output += f'{i} x R$ {valor_parcela_str}\n'
                

               
            all_output2=''
            for index, row in df.iterrows():
                
                # Convert the "Valor do seguro" column to a float by removing 'R$', and replacing the comma
    
                valorSeguro = float(row[-1][3:].replace('.', '').replace(',', '.'))
                

                # Create the result string for the current row
                result = f'''SEGURADORA {index}:\n'''+'\n'.join([f'{col}: {row[col]}' for col in df.columns])

                # Add to all_output
                all_output2 +='\n' +result + '\n'
                

                # for i in range(1, 7):
                #     # Correct the round function usage
                #     valor_parcela = round(valorSeguro / i, 2)
                #     valor_parcela_str = str(valor_parcela).replace('.', ',')
                    
                #     all_output2 += f'{i} x R$ {valor_parcela_str}\n'



            st.code(all_output_atual+all_output+'\nDEMAIS SEGURADORAS PESQUISADAS:'+all_output2+'\nAo seu dispor para esclarecimentos ou alterações necessárias.')
