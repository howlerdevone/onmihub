-- migrate:up

INSERT INTO catalog.areas (id, name) VALUES
    ('banking', 'Banking & Treasury'),
    ('project_management', 'Project Management'),
    ('social_network', 'Social Media & Marketing'),
    ('engineering', 'Engineering & Product')
ON CONFLICT (id) DO NOTHING;

INSERT INTO catalog.app_areas (app_id, area_id)
SELECT id, 'banking' FROM catalog.apps WHERE name = 'QuickBooks'
UNION ALL
SELECT id, 'project_management' FROM catalog.apps WHERE name = 'Notion'
UNION ALL
SELECT id, 'engineering' FROM catalog.apps WHERE name = 'Notion'
ON CONFLICT DO NOTHING;

-- migrate:down

DELETE FROM catalog.app_areas WHERE area_id IN ('banking', 'project_management', 'social_network', 'engineering');
DELETE FROM catalog.areas WHERE id IN ('banking', 'project_management', 'social_network', 'engineering');
