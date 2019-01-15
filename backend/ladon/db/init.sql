start transaction;

create extension if not exists ltree with schema public;


--
-- 模板表
--
create table if not exists tb_tpl (
  id serial not null primary key,
  name varchar(20) not null default 'default',
  alias varchar(100) not null,
  create_at timestamp not null default now()
);

--
-- 节点表
--
create table if not exists tb_node (
  id serial not null primary key,
  tpl_id int not null references tb_tpl(id),
  node ltree unique,
  name varchar(100) not null,
  leaf bool default true,
  metainfo json,
  op varchar(30),
  rd varchar(30),
  create_at timestamp not null default now(),
  update_at timestamp
);

--
-- 节点实例表
--
create table if not exists tb_instance (
  id serial not null primary key,
  node_id int not null references tb_node(id),
  ip varchar(20) not null,
  hostname varchar(50) not null,
  active bool default false,
  create_at timestamp not null default now(),
  update_at timestamp
);

--
-- key表
--
create table if not exists tb_key (
  id serial not null primary key,
  tpl_id int not null references tb_tpl(id),            -- 每个模板可以动态的添加key
  key varchar(50) not null,
  create_at timestamp not null default now()
);

--
-- val表
--
create table if not exists tb_val (
  id serial not null primary key,
  key_id int not null references tb_key(id),            -- 对应的key
  instance_id int not null references tb_instance(id),  -- 绑定在哪个实例上
  value varchar(100) not null,
  create_at timestamp not null default now()
);

-- 现有模板
insert into tb_tpl(name, alias) values('default', '默认模板');
insert into tb_tpl(name, alias) values('mysql', 'mysql模板');
insert into tb_tpl(name, alias) values('psql', 'psql模板');
insert into tb_tpl(name, alias) values('redis', 'redis模板');
insert into tb_tpl(name, alias) values('kafka', 'kafka模板');
insert into tb_tpl(name, alias) values('rabbitmq', 'rabbitmq模板');

-- 现有节点
insert into tb_node(tpl_id, node, name, leaf, op, rd) values(1, 'com', 'com', false, 'jinlong', 'jinlong');

commit;
