# operational Runbook - Invario

## 🚨 Critical Alerts

### `invario_ledger_integrity_status == 0`
**Severidade:** CRÍTICA (P0)
**Significado:** A corrente de hashes do Ledger foi corrompida. O hash de um bloco não bate com o `previous_hash` do seguinte.
**Ação Automática:** O endpoint `/health` retorna 503, retirando a API do load balancer.

**Procedimento de Recuperação:**

1.  **Parar a Ingestão:**
    Garanta que nenhum novo arquivo seja processado. A API já deve estar rejeitando, mas parar o container previne tentativas.
    ```bash
    docker stop invario-api
    ```

2.  **Identificar o Ponto de Ruptura:**
    Acesse o banco de dados e verifique a última transação válida verificando os hashes manualmente ou via script de auditoria.
    ```sql
    SELECT * FROM ledger_entries ORDER BY sequence_number DESC LIMIT 10;
    ```

3.  **Truncar Transações Órfãs (Último Recurso):**
    Se a corrupção ocorreu no "tip" (ponta) devido a crash durante escrita (embora `commit` atômico deva prevenir isso), você pode precisar remover a entrada corrompida para permitir que o sistema volte.

    *Cenário:* O banco confirmou a transação mas falhou ao atualizar o `ledger_head`.

    ```sql
    BEGIN;
    -- Remover entradas após o último ponto conhecido saudável
    DELETE FROM ledger_entries WHERE sequence_number > :last_good_sequence;
    -- Resetar o ledger_head
    UPDATE ledger_head SET
        last_sequence_number = :last_good_sequence,
        last_entry_hash = :hash_of_last_good_entry
    WHERE id = 1;
    COMMIT;
    ```

4.  **Reiniciar e Validar:**
    ```bash
    docker start invario-api
    curl http://localhost:8000/health
    ```
    Verifique se o status retornou para `ok` e a métrica de integridade para `1`.

### `invario_transactions_total` (Rejected > Accepted)
**Severidade:** ALTA (P1)
**Significado:** Possível ataque de fraude ou erro em arquivo de parceiro.
**Ação:** Verificar logs do `structlog` filtrando por `event="transaction_rejected"`.

---

## 🔄 Rotinas de Manutenção

### Rotação de Logs
Os logs são estruturados em JSON (stdout). O driver de log do Docker/Podman deve ser configurado para rotação.
Recomendado: `max-size: "100m"`, `max-file: "3"`.

### Backup do Banco
Realizar `pg_dump` diário da tabela `metrics` e `ledger_entries`.
```bash
docker exec invario-db pg_dump -U postgres invario > backup_$(date +%F).sql
```
