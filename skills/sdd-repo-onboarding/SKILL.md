---
name: sdd-repo-onboarding
description: Onboarding de repositório — detecta se o projeto é greenfield (novo) ou brownfield (existente) e cria os arquivos CLAUDE.md e agents.md com documentação contextualizada. Para greenfield, faz perguntas guiadas. Para brownfield, realiza engenharia reversa do código existente.
---

# SDD Repo Onboarding

Inicializa o repositório criando `CLAUDE.md` e `agents.md` a partir do contexto do projeto.

`$ARGUMENTS`: opcional — descrição breve do projeto ou `--greenfield` / `--brownfield` para forçar o modo.

## Workflow

Crie uma lista de tarefas com todos os passos abaixo e execute um por um.

---

### 1. Detectar o Modo (Greenfield ou Brownfield)

Verifique se o projeto já tem código existente:

```bash
ls -la
```

Critérios de decisão:

| Sinal | Modo sugerido |
|-------|---------------|
| Diretório vazio ou só tem `.git/` | **Greenfield** |
| Tem `package.json`, `go.mod`, `requirements.txt`, `pom.xml`, `Cargo.toml`, etc. | **Brownfield** |
| Tem pastas `src/`, `lib/`, `app/`, `cmd/` com arquivos de código | **Brownfield** |
| Argumento `--greenfield` passado | **Greenfield** (forçado) |
| Argumento `--brownfield` passado | **Brownfield** (forçado) |

Se ambos os arquivos `CLAUDE.md` e `agents.md` já existirem, pergunte ao usuário:

> "Os arquivos `CLAUDE.md` e `agents.md` já existem neste repositório. Deseja sobrescrevê-los com um onboarding completo?"

Aguarde confirmação antes de continuar.

Informe o usuário qual modo foi detectado antes de prosseguir.

---

### 2A. MODO GREENFIELD — Coleta de Informações via Perguntas

Se o modo for **Greenfield**, faça as seguintes perguntas ao usuário **em blocos** (não uma por vez — agrupe para não ser verboso):

**Bloco 1 — Visão Geral**

> "Vamos documentar o seu novo projeto! Responda o que souber:
>
> 1. **Nome do projeto**: Como ele se chama?
> 2. **Objetivo**: O que ele faz? Qual problema resolve?
> 3. **Público-alvo**: Quem vai usar? (ex: desenvolvedores internos, usuários finais, sistemas externos)
> 4. **Tipo de projeto**: (ex: API REST, aplicação web, CLI, biblioteca, microsserviço, monolito)"

Aguarde a resposta. Depois pergunte:

**Bloco 2 — Tecnologia e Arquitetura**

> "Agora sobre a stack e estrutura:
>
> 5. **Linguagem principal**: (ex: TypeScript, Python, Go, Java, Rust)
> 6. **Frameworks / bibliotecas principais**: (ex: NestJS, FastAPI, Gin, Spring Boot)
> 7. **Banco de dados**: (ex: PostgreSQL, MongoDB, Redis, sem banco)
> 8. **Infraestrutura / deploy**: (ex: AWS, GCP, Docker, Kubernetes, sem definição ainda)"

Aguarde a resposta. Depois pergunte:

**Bloco 3 — Desenvolvimento**

> "Por último, sobre convenções e fluxo de trabalho:
>
> 9. **Padrão de commits**: (ex: Conventional Commits, sem padrão definido)
> 10. **Testes**: Quais tipos serão usados? (ex: unitários com Jest, e2e com Cypress, sem testes ainda)
> 11. **Integrações externas**: Alguma API, serviço ou sistema externo relevante?
> 12. **Algo mais que Claude deve saber** ao trabalhar neste projeto?"

Aguarde a resposta e use todas as informações para os passos 3 e 4.

---

### 2B. MODO BROWNFIELD — Engenharia Reversa do Código Existente

Se o modo for **Brownfield**, explore o repositório automaticamente:

#### 2B.1 — Identificar a Stack

Verifique os arquivos de manifesto presentes:

```bash
ls -la
```

Leia os arquivos relevantes encontrados (máx. primeiras 80 linhas de cada):
- `package.json` — dependências Node.js
- `requirements.txt` / `pyproject.toml` / `setup.py` — Python
- `go.mod` — Go
- `pom.xml` / `build.gradle` — Java/Kotlin
- `Cargo.toml` — Rust
- `composer.json` — PHP
- `Gemfile` — Ruby
- `.tool-versions` / `.nvmrc` / `.python-version` — versões pinadas

#### 2B.2 — Entender a Arquitetura

Mapeie a estrutura de diretórios:

```bash
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/vendor/*' -not -path '*/__pycache__/*' \
  -not -path '*/.next/*' -not -path '*/dist/*' -not -path '*/build/*' \
  | sort | head -60
```

Leia os arquivos de configuração relevantes encontrados:
- `.eslintrc*`, `.prettierrc*` — convenções JS/TS
- `tsconfig.json` — configuração TypeScript
- `docker-compose.yml` / `Dockerfile` — infraestrutura
- `.github/workflows/*.yml` — CI/CD
- `Makefile` — comandos disponíveis
- `README.md` / `readme.md` — documentação existente

#### 2B.3 — Explorar o Código

Examine os diretórios principais de código-fonte para entender padrões:
- Leia entre 2 e 4 arquivos representativos (ex: um controller, um service, um model, um teste)
- Identifique padrões de nomenclatura, estrutura de módulos, injeção de dependência
- Observe convenções de teste (mocking, assertions, organização)
- Verifique se há middlewares, guards, interceptors, pipelines ou outros padrões transversais

#### 2B.4 — Identificar Comandos de Desenvolvimento

Extraia os comandos disponíveis de:
- `scripts` no `package.json`
- `Makefile` (alvos principais)
- Scripts na pasta `scripts/` ou `bin/`
- Comentários no `README.md`

#### 2B.5 — Resumir Descobertas

Antes de escrever os arquivos, apresente um resumo ao usuário:

> "Aqui está o que descobri sobre o projeto:
>
> - **Stack**: [tecnologias identificadas]
> - **Tipo**: [tipo de projeto]
> - **Estrutura principal**: [pastas-chave]
> - **Comandos disponíveis**: [dev, test, build, etc.]
> - **Padrões observados**: [convenções de código identificadas]
>
> Alguma correção ou informação adicional antes de eu gerar a documentação?"

Aguarde confirmação ou ajustes do usuário.

---

### 3. Escrever `agents.md`

Crie o arquivo `agents.md` na raiz do repositório com a seguinte estrutura, adaptada ao contexto do projeto:

```markdown
# Agentes — <Nome do Projeto>

Este arquivo define os perfis de agente que o Claude deve adotar ao trabalhar neste repositório.
Cada agente tem um foco, responsabilidades e restrições claras.

---

## Como usar

Invoque um agente no início de uma conversa:

> "Atue como o agente **[nome]** deste projeto."

Ou mencione implicitamente o contexto e Claude adotará o agente mais adequado.

---

## Agentes Disponíveis

### 🏗️ Arquiteto

**Quando usar:** decisões de design, estrutura de módulos, escolha de padrões, revisão de dependências.

**Responsabilidades:**
- Propor e revisar a arquitetura de novas funcionalidades
- Garantir coerência entre módulos e camadas
- Avaliar trade-offs técnicos (performance, manutenibilidade, acoplamento)
- Revisar interfaces públicas de módulos antes da implementação

**Restrições:**
- Não implementa código — apenas especifica e revisa
- Sempre considera o impacto em funcionalidades existentes antes de propor mudanças estruturais

---

### 💻 Desenvolvedor

**Quando usar:** implementação de funcionalidades, correção de bugs, refatorações.

**Responsabilidades:**
- Implementar código seguindo os padrões deste repositório
- Garantir que novos arquivos sigam as convenções de nomenclatura e estrutura existentes
- Escrever testes junto com a implementação
- Manter a cobertura de testes existente

**Restrições:**
- Não altera interfaces públicas sem revisão do Arquiteto
- Não adiciona dependências externas sem justificativa explícita
- Segue as convenções de commit definidas no `CLAUDE.md`

---

### 🧪 QA / Testador

**Quando usar:** escrita de testes, análise de cobertura, validação de comportamento.

**Responsabilidades:**
- Escrever testes unitários, de integração e e2e conforme a estratégia do projeto
- Identificar casos de borda não cobertos
- Garantir que os critérios de aceitação do SDD estejam testados
- Revisar a legibilidade e manutenibilidade dos testes

**Restrições:**
- Não altera código de produção — apenas testes e fixtures
- Reporta falhas encontradas em vez de corrigir o código de produção diretamente

---

### 🔍 Revisor de Código

**Quando usar:** revisão de PRs, análise de qualidade, identificação de problemas antes do merge.

**Responsabilidades:**
- Revisar correctude, segurança e performance do código
- Verificar aderência às convenções do projeto
- Identificar duplicação e oportunidades de simplificação
- Checar se testes cobrem os casos relevantes

**Restrições:**
- Faz sugestões claras e acionáveis — não reescreve o código do PR sem solicitação
- Distingue entre problemas bloqueantes e melhorias opcionais

---

### 🛡️ Segurança

**Quando usar:** análise de vulnerabilidades, revisão de autenticação/autorização, auditoria de dependências.

**Responsabilidades:**
- Identificar vulnerabilidades OWASP Top 10 no código
- Revisar fluxos de autenticação e autorização
- Avaliar exposição de dados sensíveis
- Verificar configurações de segurança (CORS, headers, secrets)

**Restrições:**
- Não executa exploits ou testes destrutivos
- Documenta riscos encontrados com severidade e sugestão de mitigação

---

## Comportamento Padrão

Quando nenhum agente for especificado, Claude atua como **Desenvolvedor** — implementando
com base nas convenções do projeto e nos SDDs disponíveis em `doc/features/`.
```

> Adapte os agentes ao contexto real do projeto:
> - Remova agentes que não fazem sentido (ex: se não há testes ainda, simplifique o QA)
> - Adicione agentes específicos do domínio se necessário (ex: `Data Engineer`, `DevOps`, `Mobile Developer`)
> - Use os nomes das tecnologias reais na descrição de cada agente

---

### 4. Escrever `CLAUDE.md`

Crie (ou sobrescreva) o arquivo `CLAUDE.md` na raiz do repositório com a seguinte estrutura:

```markdown
# <Nome do Projeto>

> **Documentação de agentes:** [`agents.md`](./agents.md)

<Descrição de 1-2 parágrafos: o que o projeto faz, qual problema resolve, quem usa.>

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | <ex: TypeScript 5.x> |
| Framework | <ex: NestJS 10> |
| Banco de dados | <ex: PostgreSQL 15 + Prisma ORM> |
| Testes | <ex: Jest + Supertest> |
| Infraestrutura | <ex: Docker + AWS ECS> |

---

## Estrutura do Projeto

```
<estrutura de diretórios comentada — apenas os diretórios relevantes>
```

---

## Comandos de Desenvolvimento

```bash
# Instalar dependências
<comando>

# Rodar em desenvolvimento
<comando>

# Executar testes
<comando>

# Build de produção
<comando>

# Lint e formatação
<comando>
```

---

## Arquitetura

<Descreva em 2-4 parágrafos como o projeto está organizado: camadas, módulos principais,
fluxo de dados, padrões arquiteturais usados (ex: Clean Architecture, MVC, Hexagonal).>

---

## Convenções de Código

- **Nomenclatura**: <ex: camelCase para variáveis, PascalCase para classes, kebab-case para arquivos>
- **Imports**: <ex: imports absolutos via `@/`, sem imports relativos longos>
- **Estrutura de módulo**: <ex: cada módulo tem controller, service, repository e seus testes>
- **Tratamento de erros**: <ex: exceções tipadas, sem `any` em catch>
- **Variáveis de ambiente**: <ex: todas declaradas em `.env.example`, acessadas via `ConfigService`>

---

## Convenções de Commit

<ex: Conventional Commits — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`>

---

## Integrações Externas

<Liste APIs, serviços ou sistemas externos com os quais o projeto se comunica.
Para cada um: nome, propósito, onde está configurado.>

---

## SDDs (Software Design Documents)

Funcionalidades planejadas e implementadas são documentadas em `doc/features/`:

```
doc/
  features/
    001-nome-feature/
      spec.md   ← o que construir
      plan.md   ← como construir
```

Use `/sdd <nome-da-feature>` para iniciar a documentação de uma nova funcionalidade.

---

## O que Claude deve saber

<Informações adicionais relevantes: decisões técnicas passadas, dívidas técnicas conhecidas,
áreas sensíveis do código, contexto de negócio importante, etc.>
```

> Preencha todas as seções com as informações reais coletadas nos passos anteriores.
> Remova seções que não se aplicam ao projeto. Não deixe placeholders — use conteúdo real.

---

### 5. Validar os Arquivos

Antes de commitar, verifique:

- [ ] `CLAUDE.md` não contém seções com conteúdo placeholder (`<...>`) — todas preenchidas com dados reais
- [ ] `agents.md` lista pelo menos 2 agentes relevantes para o projeto
- [ ] O link `[agents.md](./agents.md)` no `CLAUDE.md` aponta para o arquivo correto
- [ ] A stack tecnológica no `CLAUDE.md` está correta e corresponde ao projeto real
- [ ] Os comandos de desenvolvimento estão corretos e funcionais

---

### 6. Commitar

```bash
git add CLAUDE.md agents.md
git commit -m "docs: onboarding do repositório com CLAUDE.md e agents.md

- CLAUDE.md: visão geral, stack, arquitetura e convenções do projeto
- agents.md: perfis de agente para guiar o Claude no desenvolvimento"
```

---

## Encerramento

Informe ao usuário:

- **`CLAUDE.md`** criado/atualizado — documentação principal do projeto para o Claude
- **`agents.md`** criado/atualizado — perfis de agente disponíveis
- **Próximos passos sugeridos**:
  - Use `/sdd <nome-feature>` para documentar a próxima funcionalidade
  - Revise os agentes em `agents.md` e ajuste para o seu contexto
  - Mantenha o `CLAUDE.md` atualizado conforme o projeto evolui
