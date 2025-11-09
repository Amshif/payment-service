-- ================================
-- ENUM DEFINITIONS
-- ================================
CREATE TYPE payment_status AS ENUM ('created', 'authorized', 'captured', 'failed', 'refunded', 'disputed');
CREATE TYPE refund_status AS ENUM ('created', 'processed', 'failed');
CREATE TYPE settlement_status AS ENUM ('pending', 'settled', 'failed');
CREATE TYPE actor_type AS ENUM ('system', 'user', 'admin');

-- ================================
-- IDEMPOTENCY KEYS
-- ================================
CREATE TABLE idempotency_keys (
  key TEXT PRIMARY KEY,
  request_path TEXT NOT NULL,
  request_method TEXT NOT NULL,
  response_status INT,
  response_body JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ
);

-- ================================
-- PAYMENTS
-- ================================
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL,  -- reference to Order Service (no FK)
  razorpay_payment_id VARCHAR(128) UNIQUE,
  payment_gateway VARCHAR(50) DEFAULT 'razorpay', -- for multi-gateway support
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) DEFAULT 'INR',
  status payment_status NOT NULL DEFAULT 'created',
  method VARCHAR(30),
  method_details JSONB DEFAULT '{}'::jsonb,
  capture BOOLEAN DEFAULT true,
  captured_at TIMESTAMPTZ,
  payment_metadata JSONB DEFAULT '{}'::jsonb,
  idempotency_key VARCHAR(255) REFERENCES idempotency_keys(key),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status);

-- ================================
-- REFUNDS
-- ================================
CREATE TABLE refunds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  payment_id UUID NOT NULL,  -- reference to payment
  razorpay_refund_id VARCHAR(128) UNIQUE,
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) DEFAULT 'INR',
  status refund_status NOT NULL DEFAULT 'created',
  reason TEXT,
  failure_reason TEXT,
  refund_metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_refunds_payment_id ON refunds(payment_id);
CREATE INDEX idx_refunds_status ON refunds(status);

-- ================================
-- WEBHOOKS
-- ================================
CREATE TABLE webhooks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id VARCHAR(128) UNIQUE NOT NULL,
  event_type VARCHAR(128) NOT NULL,
  payload JSONB NOT NULL,
  received_at TIMESTAMPTZ DEFAULT now(),
  processed BOOLEAN DEFAULT false,
  processed_at TIMESTAMPTZ,
  processing_error TEXT
);

CREATE INDEX idx_webhooks_event_type ON webhooks(event_type);
CREATE INDEX idx_webhooks_processed ON webhooks(processed);

-- ================================
-- SETTLEMENTS (Optional)
-- ================================
CREATE TABLE settlements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  settlement_id VARCHAR(128) UNIQUE NOT NULL,
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) DEFAULT 'INR',
  status settlement_status DEFAULT 'pending',
  period_start TIMESTAMPTZ,
  period_end TIMESTAMPTZ,
  details JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_settlements_status ON settlements(status);

-- ================================
-- AUDIT LOGS (Optional)
-- ================================
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_type actor_type NOT NULL,
  actor_id UUID,
  action VARCHAR(128) NOT NULL,
  target_type VARCHAR(64),
  target_id UUID,
  before_json JSONB,
  after_json JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_type, actor_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
