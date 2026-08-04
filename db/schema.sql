\restrict dbmate

-- Dumped from database version 16.14
-- Dumped by pg_dump version 18.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: audit; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA audit;


--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA auth;


--
-- Name: billing; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA billing;


--
-- Name: catalog; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA catalog;


--
-- Name: chat; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA chat;


--
-- Name: communication; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA communication;


--
-- Name: jobs; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA jobs;


--
-- Name: organizations; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA organizations;


--
-- Name: storage; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA storage;


--
-- Name: log_level_enum; Type: TYPE; Schema: audit; Owner: -
--

CREATE TYPE audit.log_level_enum AS ENUM (
    'info',
    'warning',
    'error',
    'critical'
);


--
-- Name: provider_enum; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.provider_enum AS ENUM (
    'local',
    'google',
    'github',
    'apple',
    'microsoft'
);


--
-- Name: plan_enum; Type: TYPE; Schema: billing; Owner: -
--

CREATE TYPE billing.plan_enum AS ENUM (
    'free',
    'pro'
);


--
-- Name: message_sender_enum; Type: TYPE; Schema: chat; Owner: -
--

CREATE TYPE chat.message_sender_enum AS ENUM (
    'user',
    'bot',
    'system'
);


--
-- Name: message_source_enum; Type: TYPE; Schema: chat; Owner: -
--

CREATE TYPE chat.message_source_enum AS ENUM (
    'web',
    'whatsapp',
    'telegram'
);


--
-- Name: task_status_enum; Type: TYPE; Schema: jobs; Owner: -
--

CREATE TYPE jobs.task_status_enum AS ENUM (
    'queued',
    'running',
    'completed',
    'failed'
);


--
-- Name: workspace_role_enum; Type: TYPE; Schema: organizations; Owner: -
--

CREATE TYPE organizations.workspace_role_enum AS ENUM (
    'owner',
    'admin',
    'member'
);


--
-- Name: file_status_enum; Type: TYPE; Schema: storage; Owner: -
--

CREATE TYPE storage.file_status_enum AS ENUM (
    'pending',
    'processing',
    'ready',
    'failed'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_logs; Type: TABLE; Schema: audit; Owner: -
--

CREATE TABLE audit.activity_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    action character varying(100) NOT NULL,
    entity_type character varying(50) NOT NULL,
    entity_id uuid NOT NULL,
    ip_address character varying(45),
    user_agent text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: system_errors; Type: TABLE; Schema: audit; Owner: -
--

CREATE TABLE audit.system_errors (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    level audit.log_level_enum DEFAULT 'error'::audit.log_level_enum NOT NULL,
    endpoint character varying(255),
    method character varying(10),
    error_message text NOT NULL,
    traceback text,
    user_id uuid,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: accounts; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.accounts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    provider auth.provider_enum NOT NULL,
    provider_user_id character varying(255) NOT NULL,
    access_token text,
    refresh_token text,
    expires_at timestamp with time zone,
    scope text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email text,
    display_name text,
    avatar_url text,
    preferred_language text,
    timezone text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: plan_limits; Type: TABLE; Schema: billing; Owner: -
--

CREATE TABLE billing.plan_limits (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    plan_id billing.plan_enum NOT NULL,
    limit_key character varying(100) NOT NULL,
    limit_value bigint NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: plans; Type: TABLE; Schema: billing; Owner: -
--

CREATE TABLE billing.plans (
    id billing.plan_enum NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: subscriptions; Type: TABLE; Schema: billing; Owner: -
--

CREATE TABLE billing.subscriptions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    workspace_id uuid NOT NULL,
    plan_id billing.plan_enum NOT NULL,
    status character varying(50) DEFAULT 'active'::character varying NOT NULL,
    current_period_end timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: app_areas; Type: TABLE; Schema: catalog; Owner: -
--

CREATE TABLE catalog.app_areas (
    app_id character varying(50) NOT NULL,
    area_id character varying(50) NOT NULL
);


--
-- Name: apps; Type: TABLE; Schema: catalog; Owner: -
--

CREATE TABLE catalog.apps (
    id character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    icon_url text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: areas; Type: TABLE; Schema: catalog; Owner: -
--

CREATE TABLE catalog.areas (
    id character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: conversations; Type: TABLE; Schema: chat; Owner: -
--

CREATE TABLE chat.conversations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    workspace_id uuid NOT NULL,
    title character varying(255) DEFAULT 'New Conversation'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: messages; Type: TABLE; Schema: chat; Owner: -
--

CREATE TABLE chat.messages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    conversation_id uuid NOT NULL,
    sender chat.message_sender_enum NOT NULL,
    source chat.message_source_enum DEFAULT 'web'::chat.message_source_enum NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: channels; Type: TABLE; Schema: communication; Owner: -
--

CREATE TABLE communication.channels (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    platform character varying(30) NOT NULL,
    platform_chat_id character varying(100) NOT NULL,
    verification_code character varying(10),
    is_verified boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: background_tasks; Type: TABLE; Schema: jobs; Owner: -
--

CREATE TABLE jobs.background_tasks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    celery_task_id uuid,
    task_name character varying(150) NOT NULL,
    status jobs.task_status_enum DEFAULT 'queued'::jobs.task_status_enum NOT NULL,
    progress_percentage integer DEFAULT 0 NOT NULL,
    meta_payload jsonb,
    error_details text,
    workspace_id uuid NOT NULL,
    user_id uuid,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT background_tasks_progress_percentage_check CHECK (((progress_percentage >= 0) AND (progress_percentage <= 100)))
);


--
-- Name: memberships; Type: TABLE; Schema: organizations; Owner: -
--

CREATE TABLE organizations.memberships (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    workspace_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role organizations.workspace_role_enum DEFAULT 'member'::organizations.workspace_role_enum NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: permissions; Type: TABLE; Schema: organizations; Owner: -
--

CREATE TABLE organizations.permissions (
    id character varying(50) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: role_permissions; Type: TABLE; Schema: organizations; Owner: -
--

CREATE TABLE organizations.role_permissions (
    role organizations.workspace_role_enum NOT NULL,
    permission_id character varying(50) NOT NULL
);


--
-- Name: workspaces; Type: TABLE; Schema: organizations; Owner: -
--

CREATE TABLE organizations.workspaces (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(120) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by uuid
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: files; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.files (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    owner_id uuid NOT NULL,
    parent_id uuid,
    is_folder boolean DEFAULT false NOT NULL,
    name character varying(255) NOT NULL,
    storage_path text,
    mime_type character varying(100),
    size_bytes bigint DEFAULT 0,
    status storage.file_status_enum DEFAULT 'pending'::storage.file_status_enum NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- Name: system_errors system_errors_pkey; Type: CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.system_errors
    ADD CONSTRAINT system_errors_pkey PRIMARY KEY (id);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: accounts unique_provider_identity; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.accounts
    ADD CONSTRAINT unique_provider_identity UNIQUE (provider, provider_user_id);


--
-- Name: accounts unique_user_provider; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.accounts
    ADD CONSTRAINT unique_user_provider UNIQUE (user_id, provider);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: plan_limits plan_limits_pkey; Type: CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.plan_limits
    ADD CONSTRAINT plan_limits_pkey PRIMARY KEY (id);


--
-- Name: plans plans_pkey; Type: CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_workspace_id_key; Type: CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.subscriptions
    ADD CONSTRAINT subscriptions_workspace_id_key UNIQUE (workspace_id);


--
-- Name: plan_limits unique_plan_limit_key; Type: CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.plan_limits
    ADD CONSTRAINT unique_plan_limit_key UNIQUE (plan_id, limit_key);


--
-- Name: app_areas app_areas_pkey; Type: CONSTRAINT; Schema: catalog; Owner: -
--

ALTER TABLE ONLY catalog.app_areas
    ADD CONSTRAINT app_areas_pkey PRIMARY KEY (app_id, area_id);


--
-- Name: apps apps_pkey; Type: CONSTRAINT; Schema: catalog; Owner: -
--

ALTER TABLE ONLY catalog.apps
    ADD CONSTRAINT apps_pkey PRIMARY KEY (id);


--
-- Name: areas areas_pkey; Type: CONSTRAINT; Schema: catalog; Owner: -
--

ALTER TABLE ONLY catalog.areas
    ADD CONSTRAINT areas_pkey PRIMARY KEY (id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: chat; Owner: -
--

ALTER TABLE ONLY chat.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: chat; Owner: -
--

ALTER TABLE ONLY chat.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: channels channels_pkey; Type: CONSTRAINT; Schema: communication; Owner: -
--

ALTER TABLE ONLY communication.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (id);


--
-- Name: channels unique_platform_chat_identity; Type: CONSTRAINT; Schema: communication; Owner: -
--

ALTER TABLE ONLY communication.channels
    ADD CONSTRAINT unique_platform_chat_identity UNIQUE (platform, platform_chat_id);


--
-- Name: channels unique_user_platform_channel; Type: CONSTRAINT; Schema: communication; Owner: -
--

ALTER TABLE ONLY communication.channels
    ADD CONSTRAINT unique_user_platform_channel UNIQUE (user_id, platform);


--
-- Name: background_tasks background_tasks_celery_task_id_key; Type: CONSTRAINT; Schema: jobs; Owner: -
--

ALTER TABLE ONLY jobs.background_tasks
    ADD CONSTRAINT background_tasks_celery_task_id_key UNIQUE (celery_task_id);


--
-- Name: background_tasks background_tasks_pkey; Type: CONSTRAINT; Schema: jobs; Owner: -
--

ALTER TABLE ONLY jobs.background_tasks
    ADD CONSTRAINT background_tasks_pkey PRIMARY KEY (id);


--
-- Name: memberships memberships_pkey; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.memberships
    ADD CONSTRAINT memberships_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role, permission_id);


--
-- Name: memberships unique_user_workspace_membership; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.memberships
    ADD CONSTRAINT unique_user_workspace_membership UNIQUE (workspace_id, user_id);


--
-- Name: workspaces workspaces_pkey; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.workspaces
    ADD CONSTRAINT workspaces_pkey PRIMARY KEY (id);


--
-- Name: workspaces workspaces_slug_key; Type: CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.workspaces
    ADD CONSTRAINT workspaces_slug_key UNIQUE (slug);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: files unique_filename_per_folder; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.files
    ADD CONSTRAINT unique_filename_per_folder UNIQUE (owner_id, parent_id, name, is_folder);


--
-- Name: idx_audit_activity_logs_target; Type: INDEX; Schema: audit; Owner: -
--

CREATE INDEX idx_audit_activity_logs_target ON audit.activity_logs USING btree (entity_type, entity_id);


--
-- Name: idx_audit_activity_logs_user_action; Type: INDEX; Schema: audit; Owner: -
--

CREATE INDEX idx_audit_activity_logs_user_action ON audit.activity_logs USING btree (user_id, action);


--
-- Name: idx_audit_system_errors_level; Type: INDEX; Schema: audit; Owner: -
--

CREATE INDEX idx_audit_system_errors_level ON audit.system_errors USING btree (level);


--
-- Name: idx_audit_system_errors_user; Type: INDEX; Schema: audit; Owner: -
--

CREATE INDEX idx_audit_system_errors_user ON audit.system_errors USING btree (user_id);


--
-- Name: idx_auth_accounts_lookup; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_auth_accounts_lookup ON auth.accounts USING btree (provider, provider_user_id);


--
-- Name: idx_auth_accounts_user_id; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_auth_accounts_user_id ON auth.accounts USING btree (user_id);


--
-- Name: idx_auth_users_email; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_auth_users_email ON auth.users USING btree (email);


--
-- Name: idx_billing_plan_limits_lookup; Type: INDEX; Schema: billing; Owner: -
--

CREATE INDEX idx_billing_plan_limits_lookup ON billing.plan_limits USING btree (plan_id, limit_key);


--
-- Name: idx_billing_subscriptions_workspace; Type: INDEX; Schema: billing; Owner: -
--

CREATE INDEX idx_billing_subscriptions_workspace ON billing.subscriptions USING btree (workspace_id);


--
-- Name: idx_catalog_app_areas_lookup; Type: INDEX; Schema: catalog; Owner: -
--

CREATE INDEX idx_catalog_app_areas_lookup ON catalog.app_areas USING btree (area_id);


--
-- Name: idx_chat_messages_chronological_sequence; Type: INDEX; Schema: chat; Owner: -
--

CREATE INDEX idx_chat_messages_chronological_sequence ON chat.messages USING btree (conversation_id, created_at);


--
-- Name: idx_communication_channels_webhook_lookup; Type: INDEX; Schema: communication; Owner: -
--

CREATE INDEX idx_communication_channels_webhook_lookup ON communication.channels USING btree (platform, platform_chat_id) WHERE (is_verified = true);


--
-- Name: idx_jobs_background_tasks_celery; Type: INDEX; Schema: jobs; Owner: -
--

CREATE INDEX idx_jobs_background_tasks_celery ON jobs.background_tasks USING btree (celery_task_id);


--
-- Name: idx_jobs_background_tasks_status; Type: INDEX; Schema: jobs; Owner: -
--

CREATE INDEX idx_jobs_background_tasks_status ON jobs.background_tasks USING btree (status);


--
-- Name: idx_jobs_background_tasks_workspace; Type: INDEX; Schema: jobs; Owner: -
--

CREATE INDEX idx_jobs_background_tasks_workspace ON jobs.background_tasks USING btree (workspace_id);


--
-- Name: idx_organizations_memberships_user; Type: INDEX; Schema: organizations; Owner: -
--

CREATE INDEX idx_organizations_memberships_user ON organizations.memberships USING btree (user_id);


--
-- Name: idx_organizations_memberships_workspace; Type: INDEX; Schema: organizations; Owner: -
--

CREATE INDEX idx_organizations_memberships_workspace ON organizations.memberships USING btree (workspace_id);


--
-- Name: idx_organizations_workspaces_created_by; Type: INDEX; Schema: organizations; Owner: -
--

CREATE INDEX idx_organizations_workspaces_created_by ON organizations.workspaces USING btree (created_by);


--
-- Name: idx_storage_files_owner; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_storage_files_owner ON storage.files USING btree (owner_id);


--
-- Name: idx_storage_files_parent; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_storage_files_parent ON storage.files USING btree (parent_id);


--
-- Name: idx_storage_files_status; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_storage_files_status ON storage.files USING btree (status);


--
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: system_errors system_errors_user_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.system_errors
    ADD CONSTRAINT system_errors_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE SET NULL;


--
-- Name: accounts accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.accounts
    ADD CONSTRAINT accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: plan_limits plan_limits_plan_id_fkey; Type: FK CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.plan_limits
    ADD CONSTRAINT plan_limits_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES billing.plans(id) ON DELETE CASCADE;


--
-- Name: subscriptions subscriptions_plan_id_fkey; Type: FK CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.subscriptions
    ADD CONSTRAINT subscriptions_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES billing.plans(id);


--
-- Name: subscriptions subscriptions_workspace_id_fkey; Type: FK CONSTRAINT; Schema: billing; Owner: -
--

ALTER TABLE ONLY billing.subscriptions
    ADD CONSTRAINT subscriptions_workspace_id_fkey FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE;


--
-- Name: app_areas app_areas_app_id_fkey; Type: FK CONSTRAINT; Schema: catalog; Owner: -
--

ALTER TABLE ONLY catalog.app_areas
    ADD CONSTRAINT app_areas_app_id_fkey FOREIGN KEY (app_id) REFERENCES catalog.apps(id) ON DELETE CASCADE;


--
-- Name: app_areas app_areas_area_id_fkey; Type: FK CONSTRAINT; Schema: catalog; Owner: -
--

ALTER TABLE ONLY catalog.app_areas
    ADD CONSTRAINT app_areas_area_id_fkey FOREIGN KEY (area_id) REFERENCES catalog.areas(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_workspace_id_fkey; Type: FK CONSTRAINT; Schema: chat; Owner: -
--

ALTER TABLE ONLY chat.conversations
    ADD CONSTRAINT conversations_workspace_id_fkey FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE;


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: chat; Owner: -
--

ALTER TABLE ONLY chat.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES chat.conversations(id) ON DELETE CASCADE;


--
-- Name: channels channels_user_id_fkey; Type: FK CONSTRAINT; Schema: communication; Owner: -
--

ALTER TABLE ONLY communication.channels
    ADD CONSTRAINT channels_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: background_tasks background_tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: jobs; Owner: -
--

ALTER TABLE ONLY jobs.background_tasks
    ADD CONSTRAINT background_tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE SET NULL;


--
-- Name: background_tasks background_tasks_workspace_id_fkey; Type: FK CONSTRAINT; Schema: jobs; Owner: -
--

ALTER TABLE ONLY jobs.background_tasks
    ADD CONSTRAINT background_tasks_workspace_id_fkey FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE;


--
-- Name: workspaces fk_organizations_workspaces_created_by; Type: FK CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.workspaces
    ADD CONSTRAINT fk_organizations_workspaces_created_by FOREIGN KEY (created_by) REFERENCES auth.users(id) ON DELETE SET NULL;


--
-- Name: memberships memberships_user_id_fkey; Type: FK CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.memberships
    ADD CONSTRAINT memberships_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: memberships memberships_workspace_id_fkey; Type: FK CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.memberships
    ADD CONSTRAINT memberships_workspace_id_fkey FOREIGN KEY (workspace_id) REFERENCES organizations.workspaces(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: organizations; Owner: -
--

ALTER TABLE ONLY organizations.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES organizations.permissions(id) ON DELETE CASCADE;


--
-- Name: files files_owner_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.files
    ADD CONSTRAINT files_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: files files_parent_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.files
    ADD CONSTRAINT files_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES storage.files(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict dbmate


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20260731185800'),
    ('20260731190303'),
    ('20260731195507'),
    ('20260731201542'),
    ('20260731202647'),
    ('20260731205049'),
    ('20260731205306'),
    ('20260731210918'),
    ('20260731211312'),
    ('20260803123000');
