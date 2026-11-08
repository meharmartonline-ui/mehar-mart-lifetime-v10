-- MEHAR MART V94 SUPABASE SCHEMA
-- Run this whole script once in Supabase Dashboard -> SQL Editor -> New query.
-- V94 uses a server-side Supabase secret key stored in Streamlit Secrets.
-- Do NOT expose the secret key in browser/client code.

create table if not exists public.products (
    id text primary key,
    data jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.orders (
    id text primary key,
    data jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.app_settings (
    id text primary key,
    data jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists products_updated_at on public.products;
create trigger products_updated_at before update on public.products
for each row execute function public.set_updated_at();

drop trigger if exists orders_updated_at on public.orders;
create trigger orders_updated_at before update on public.orders
for each row execute function public.set_updated_at();

drop trigger if exists app_settings_updated_at on public.app_settings;
create trigger app_settings_updated_at before update on public.app_settings
for each row execute function public.set_updated_at();

-- RLS is enabled. V94's server-only secret key accesses these tables.
alter table public.products enable row level security;
alter table public.orders enable row level security;
alter table public.app_settings enable row level security;

-- No anonymous/public policies are created. Customers access data through
-- the Streamlit server, not directly from the browser.
