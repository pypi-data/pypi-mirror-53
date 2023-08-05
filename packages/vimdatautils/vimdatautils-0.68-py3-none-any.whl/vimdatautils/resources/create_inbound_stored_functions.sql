
create or replace function sf_execute_if_table_exists(p_table_name varchar, p_ddl_script varchar) returns void as
$$
begin
    if (select to_regclass(p_table_name) is not null)
    then
        raise notice 'about to execute script: %s', p_ddl_script;
        execute p_ddl_script;
    else
        raise notice 'table %s doesn''t exist', p_table_name;
    end if;
end;
$$ language plpgsql;

create or replace function sf_hash_salt(p_domain_hash_salt varchar, p_column varchar) returns varchar as
$$
begin
    return (select encode(digest(p_domain_hash_salt || encode(concat_ws(' ', p_column)::bytea, 'base64'), 'sha256'),'hex'));
end;
$$ language plpgsql;
