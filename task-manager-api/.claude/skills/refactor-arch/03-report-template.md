# Referência: Template de Relatório de Auditoria

Use este formato exato para o relatório de auditoria da Fase 2:

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================
Project: [nome do projeto]
Stack:   [Linguagem] + [Framework]
Files:   [N] analyzed | ~[X] lines of code

## Summary
CRITICAL: [N] | HIGH: [N] | MEDIUM: [N] | LOW: [N]

## Findings

### [CRITICAL] [Nome do Anti-Pattern]
File: [arquivo]:[linha_inicio]-[linha_fim]
Description: [Descrição concisa do problema encontrado]
Impact: [Consequência prática do problema]
Recommendation: [Ação recomendada]

### [HIGH] [Nome do Anti-Pattern]
File: [arquivo]:[linha_inicio]-[linha_fim]
Description: [Descrição concisa]
Impact: [Consequência]
Recommendation: [Ação]

### [MEDIUM] [Nome do Anti-Pattern]
File: [arquivo]:[linha]
Description: [Descrição concisa]
Impact: [Consequência]
Recommendation: [Ação]

### [LOW] [Nome do Anti-Pattern]
File: [arquivo]:[linha]
Description: [Descrição concisa]
Impact: [Consequência]
Recommendation: [Ação]

================================
Total: [N] findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Regras do Template

1. **Ordenação**: Findings DEVEM ser ordenados por severidade (CRITICAL primeiro, LOW por último)
2. **Localização**: Cada finding DEVE ter arquivo e linhas exatos
3. **Mínimo**: O relatório DEVE ter no mínimo 5 findings
4. **Severidade**: DEVE incluir pelo menos 1 CRITICAL ou HIGH
5. **Confirmação**: OBRIGATÓRIO perguntar antes de prosseguir para Fase 3
6. **Deprecated APIs**: Se houver uso de APIs deprecated, DEVE ser reportado como finding
