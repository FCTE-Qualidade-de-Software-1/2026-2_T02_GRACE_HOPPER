# Homenagem a Grace Hopper (1906–1992)

<div class="gh-hero-split" markdown>
<div class="gh-hero-split__texto" markdown>

<p class="gh-hero-split__eyebrow">Identidade da Equipe · Pioneiros da Engenharia e Qualidade de Software</p>

<h1 class="gh-hero-split__title">Grace Brewster Murray <span>Hopper</span></h1>

<p class="gh-hero-split__lead">Matemática, cientista da computação e Contra-Almirante da Marinha dos Estados Unidos. Criadora do primeiro compilador da história (<code>A-0</code>), idealizadora da programação independente de máquina que deu origem ao <code>COBOL</code> e pioneira da verificação e padronização de software.</p>

<p class="gh-transparencia">
  <em>"A frase mais perigosa da língua é: 'Nós sempre fizemos assim'."</em> — Grace Hopper
</p>

</div>
<figure class="gh-retrato">
  <img src="../../assets/images/grace-hopper.jpg" alt="Retrato oficial de Grace Hopper em uniforme da Marinha dos Estados Unidos." width="771" height="1025">
  <figcaption>
    <strong>Contra-Almirante Grace M. Hopper, USN</strong>
    <a href="https://commons.wikimedia.org/wiki/File:Commodore_Grace_M._Hopper,_USN_(covered)_head_and_shoulders_crop.jpg" target="_blank" rel="noopener">Fotografia histórica: U.S. Navy (Domínio Público)</a>
  </figcaption>
</figure>
</div>

---

## 1. Trajetória Acadêmica e Pioneirismo na Computação

Nascida em Nova York em 9 de dezembro de 1906, **Grace Brewster Murray Hopper** graduou-se em Matemática e Física pelo Vassar College (1928) e obteve o mestrado (1930) e o doutorado em Matemática pela **Universidade Yale** (1934).

Durante a Segunda Guerra Mundial, ingressou na reserva da Marinha dos Estados Unidos (WAVES) e foi designada em 1944 para o projeto de computação do laboratório Cruft na **Universidade Harvard**, onde trabalhou com Howard Aiken na programação do computador eletromecânico **Harvard Mark I** — redigindo o primeiro manual completo de operação e programação de computadores da história (*A Manual of Operation for the Automatic Sequence Controlled Calculator*).

---

## 2. Contribuições Diretas para a Engenharia e Qualidade de Software

### 2.1. O Primeiro Compilador (`A-0`) e a Redução de Defeitos Humanos
Em 1952, enquanto trabalhava na Eckert-Mauchly Computer Corporation (desenvolvedora do UNIVAC I), Grace Hopper criou o sistema **`A-0`**, o primeiro compilador da história. Em uma época em que engenheiros acreditavam que computadores só podiam realizar aritmética e que todo código precisava ser escrito em octal ou binário, Hopper demonstrou que programas poderiam ser escritos em alto nível e traduzidos automaticamente, reduzindo drasticamente a taxa de defeitos de codificação e elevando a **analisabilidade e manutenibilidade** do software.

### 2.2. O Registro Histórico do Primeiro "Bug" Documentado (1947)
Em 9 de setembro de 1947, a equipe de Grace Hopper no computador **Harvard Mark II** investigava uma falha no relé nº 70 do Painel F quando encontrou uma mariposa (*moth*) presa nos contatos eletromecânicos. O inseto foi colado no livro de registros (*logbook*) do laboratório com a anotação *"First actual case of bug being found"* (hoje preservado no Smithsonian Institution). Esse episódio popularizou na computação os termos **bug** (defeito/falha) e **debugging** (depuração sistemática Baseada em evidências).

### 2.3. Padronização e Certificação de Compiladores `COBOL`
A partir do compilador `FLOW-MATIC`, Grace Hopper liderou a base técnica que originou a linguagem **`COBOL`** (*Common Business-Oriented Language*) em 1959. Mais tarde, de volta ao serviço ativo na Marinha nas décadas de 1960 e 1970, Hopper liderou o desenvolvimento de **suítes padronizadas de validação e testes de conformidade** para compiladores COBOL em toda a Marinha e no Departamento de Defesa dos EUA — um dos primeiros programas institucionais de **avaliação de conformidade e interoperabilidade de software** em larga escala, precursor direto do que hoje é normatizado pela família **ISO/IEC 25000 (SQuaRE)**.

### 2.4. Os "Fios de Nanossegundo" e a Tangibilidade das Métricas
Como educadora incansável, Grace Hopper distribuía em suas palestras pedaços de fio de cobre com aproximadamente $29{,}98\text{ cm}$ ($11{,}8\text{ polegadas}$) — a distância máxima que a luz ou um sinal elétrico percorre em um bilionésimo de segundo (**um nanossegundo**). Com esse artefato simples, ela ensinava engenheiros e almirantes que **métricas abstratas de software precisam ser traduzidas em evidências concretas e compreensíveis para quem toma decisões**.

---

## 3. Conexão com o Nosso Projeto (Avaliação do i-Educar)

O espírito do trabalho de Grace Hopper guia diretamente nossa avaliação do **i-Educar**:

1. **Rigor na Verificação de Sistemas Administrativos (`COBOL` → Gestão Escolar):** Assim como Hopper dedicou sua carreira a tornar os sistemas de processamento de dados governamentais legíveis, padronizados e livres de falhas de cálculo, avaliamos no **i-Educar** o determinismo do cálculo de notas (`Gate M3`), a integridade das transações (`Gate M4`) e os contratos de interoperabilidade (`M2`).
2. **Tradução de Métricas Técnicas em Decisões Claras:** Seguindo a lição dos "fios de nanossegundo", estruturamos nosso [Framework GQM](../fase-2/index.md) e nosso [Painel PSM/CID](../indicadores_psm.md) para transformar métricas de código e processo em indicadores objetivos de decisão para Secretarias Municipais de Educação e mantenedores.
