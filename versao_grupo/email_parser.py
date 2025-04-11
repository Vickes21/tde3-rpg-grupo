import os
import re

def parse_email_file(file_path):
    """
    Analisa um arquivo de email para extrair remetente e destinatários.
    
    Args:
        file_path: Caminho para o arquivo de email
        
    Returns:
        tuple: (remetente, destinatários), onde remetente é uma string e destinatários é uma lista
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Extrai o remetente
            sender_match = re.search(r'From:.*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
            if not sender_match:
                return None, None
            
            sender = sender_match.group(1).lower()
            
            # Extrai destinatários do campo To:
            recipients = []
            
            # Extrai do campo To: - usando âncora de início de linha para evitar X-To:
            to_matches = re.findall(r'(?:^|\n)To:.*?((?:<?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}>?,?\s*)+)', content, re.MULTILINE)
            if to_matches:
                # Extrai os emails individuais de cada linha To:
                email_pattern = r'<?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>?'
                for match in to_matches:
                    emails = re.findall(email_pattern, match)
                    recipients.extend([email.lower() for email in emails])
            
            # Se nenhum destinatário for encontrado, retorna None
            if not recipients:
                return None, None
            
            return sender, recipients
        
    except Exception as e:
        print(f"Erro ao analisar o arquivo {file_path}: {e}")
        return None, None

def build_graph_from_emails(graph, root_folder):
    """
    Constrói um grafo a partir de emails na pasta especificada.
    
    Args:
        graph: O objeto de grafo a preencher
        root_folder: A pasta raiz contendo os emails
        
    Retorna:
        graph: O grafo preenchido
    """
    # Percorre todos os diretórios e arquivos
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Tenta analisar todos os arquivos como emails
            sender, recipients = parse_email_file(file_path)
            
            if sender and recipients:
                for recipient in recipients:
                    graph.add_edge(sender, recipient)
    
    return graph
