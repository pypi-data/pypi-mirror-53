
create table if not exists update_log (
  id serial primary key,
  table_name varchar not null,
  entities_count integer not null,
  update_date timestamp without time zone not null default now()
);
