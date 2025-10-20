-- ================================
-- ENUM DEFINITIONS
-- ================================
CREATE TYPE order_status AS ENUM ('created', 'paid', 'partially_paid', 'failed', 'cancelled', 'refunded');
CREATE TYPE payment_status AS ENUM ('created', 'authorized', 'captured', 'failed', 'refunded', 'disputed');
CREATE TYPE refund_status AS ENUM ('created', 'processed', 'failed');
CREATE TYPE settlement_status AS ENUM ('pending', 'settled', 'failed');
CREATE TYPE actor_type AS ENUM ('system', 'user', 'admin');
CREATE TYPE user_role AS ENUM ('user', 'admin', 'support');

-- ================================
-- USERS
-- ================================
CREATE EXTENSION IF NOT EXISTS citext;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email CITEXT UNIQUE NOT NULL,
  phone VARCHAR(20),
  name VARCHAR(255),
  role user_role NOT NULL DEFAULT 'user',
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ================================
-- ORDERS
-- ================================
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_order_id VARCHAR(128) UNIQUE NOT NULL,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) NOT NULL DEFAULT 'INR',
  status order_status NOT NULL DEFAULT 'created',
  razorpay_order_id VARCHAR(128) UNIQUE,
  description TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ================================
-- PAYMENTS
-- ================================
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  razorpay_payment_id VARCHAR(128) UNIQUE,
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) DEFAULT 'INR',
  status payment_status NOT NULL DEFAULT 'created',
  method VARCHAR(30),
  method_details JSONB DEFAULT '{}'::jsonb,
  capture BOOLEAN DEFAULT true,
  captured_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  idempotency_key VARCHAR(255) REFERENCES idempotency_keys(key)
);

-- ================================
-- REFUNDS
-- ================================
CREATE TABLE refunds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  payment_id UUID NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
  razorpay_refund_id VARCHAR(128) UNIQUE,
  amount BIGINT NOT NULL CHECK (amount > 0),
  currency CHAR(3) DEFAULT 'INR',
  status refund_status NOT NULL DEFAULT 'created',
  failure_reason TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

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
-- IDEMPOTENCY KEYS
-- ================================
CREATE TABLE idempotency_keys (
  key TEXT PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  request_path TEXT NOT NULL,
  request_method TEXT NOT NULL,
  response_status INT,
  response_body JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ
);

-- ================================
-- SETTLEMENTS
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

-- ================================
-- AUDIT LOGS
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
