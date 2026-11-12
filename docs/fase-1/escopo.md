# Escopo, Profundidade e Objetos de Avaliação

Em atendimento à Atividade 1.4 da **ISO/IEC 25040:2024**, esta seção delimita de forma explícita **o que entra** e **o que fica de fora** da avaliação, bem como os níveis de profundidade técnica adotados.

---

## 1. Níveis de Profundidade da Avaliação

A inspeção combina três perspectivas complementares sobre os módulos de **Matrícula de Alunos** e **Lançamento de Notas e Menções**:

1. **Caixa-Branca (Código-Fonte e Testes Automatizados):** Inspeção direta da árvore sintática, controle de fluxo e acoplamento em `app/Services/RegistrationService.php`, `ieducar/modules/Avaliacao/Service/Boletim.php`, `DiarioController.php`, `DiarioApiController.php`, modelos `app/Models/Legacy*.php` e suíte de testes Pest/PHPUnit (`M7a` a `M11`).
2. **Caixa-Cinza (Banco de Dados, Transações e Contratos de API):** Validação de esquemas JSON REST (`M2`), injeção controlada de falhas intermediárias com auditoria SQL das tabelas `pmieducar.*` e `modules.*` (`M4`), coexistência de recursos em containers (`M1`) e restauração de dumps `pg_dump` (`M6`).
3. **Caixa-Preta e Qualidade em Uso (Interface e Sessões Guiadas):** Submissão de catálogos de entradas inválidas (`M12`), avaliação independente de clareza de mensagens (`M13`) e execução cronometrada das tarefas `T1` (Matrícula) e `T2` (Diário) por usuários iniciantes sob TCLE (`M14a`, `M14b` e `M15`).

---

## 2. Quadro de Delimitação: Dentro vs. Fora do Escopo

**Tabela 1 — Objetos incluídos, exclusões declaradas e justificativas de corte**

| Dimensão | O que Entra no Escopo (Incluído) | O que Fica de Fora do Escopo (Excluído) | Justificativa Técnica do Recorte |
| :--- | :--- | :--- | :--- |
| **Módulos Funcionais** | **Matrícula de Alunos** (vínculo, enturmação, remanejamento, situações) e **Lançamento de Notas e Menções** (regras de avaliação, arredondamento, diário e cálculo de médias). | Biblioteca escolar, transporte escolar, alimentação/merenda, alocação de servidores/RH e relatórios gerenciais secundários. | Matrícula e Avaliação formam o núcleo acadêmico obrigatório cuja falha invalida o histórico escolar e o Censo. |
| **Integrações Externas** | Endpoints da API REST interna (`routes/api.php` e `ieducar/modules/Api/`) voltados a matrícula e diário (`M2 — CEI`). | Pacote externo `portabilis/i-educar-educacenso-package` e sincronização com servidores externos do MEC/INEP. | O exportador do Educacenso vive em repositório separado; seu impacto é tratado indiretamente pela integridade das tabelas base (`G2`). |
| **Infraestrutura e Escala** | Coexistência de 2 instâncias locais parametrizadas via `.env` (`M1`) e backup/restore no PostgreSQL 18 (`M6`). | Testes de carga/estresse distribuídos para centenas de escolas simultâneas e alta disponibilidade em nuvem (Kubernetes/AWS). | Ambiente laboratorial local não reproduz topologia de rede municipal de larga escala sem distorcer medidas de latência. |
| **Segurança e Privacidade** | Prevenção contra entradas inválidas de domínio (`M12`) e uso exclusivo de dados fictícios e participantes anonimizados sob LGPD/TCLE. | Testes de intrusão (*pentest*), análise de vulnerabilidades de rede/WAF e auditoria criptográfica de autenticação. | O foco da avaliação é a integridade funcional, estrutural e de interação dos registros pedagógicos. |

*Fonte: Elaborado pelos autores.*
