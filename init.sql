-- TABELA: clients

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================
-- TABELA: postings

CREATE TABLE IF NOT EXISTS postings (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    weight_kg NUMERIC(10,2) NOT NULL,
    volume_cm3 NUMERIC(10,2) NOT NULL,
    freight_price NUMERIC(10,2) NOT NULL,
    tracking_code TEXT NOT NULL UNIQUE,

    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    shipped_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,

    CONSTRAINT fk_postings_client
        FOREIGN KEY (client_id)
        REFERENCES clients (id)
        ON DELETE CASCADE,

    CONSTRAINT chk_posting_status
        CHECK (status IN ('pending', 'shipped', 'delivered'))
);

-- ============================
-- TABELA: status_history

CREATE TABLE IF NOT EXISTS status_history (
    id SERIAL PRIMARY KEY,
    posting_id INTEGER NOT NULL,
    old_status TEXT NOT NULL,
    new_status TEXT NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_status_history_posting
        FOREIGN KEY (posting_id)
        REFERENCES postings (id)
        ON DELETE CASCADE,

    CONSTRAINT chk_old_status
        CHECK (old_status IN ('pending', 'shipped', 'delivered')),

    CONSTRAINT chk_new_status
        CHECK (new_status IN ('pending', 'shipped', 'delivered'))
);
