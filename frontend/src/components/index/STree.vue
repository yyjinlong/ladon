<template>
  <div class="stree" @mousedown="mouse_down($event)">
    <Split v-model="split_rate" min="285px">
      <div slot="left" class="split-pane">
        <Input search placeholder='lucene语法,如"10.11.10.2"或host: "app10"'
               v-model="lucene" @on-enter="global_search" />
        <div id="service_tree" class="ztree"></div>
      </div>
      <div slot="right" class="split-right-pane">
        <Breadcrumb :style="{padding: '10px'}">
          <BreadcrumbItem to="/">服务树</BreadcrumbItem>
          <BreadcrumbItem>{{ tip_node }}</BreadcrumbItem>
        </Breadcrumb>
        <Divider :style="{margin: '0 0 10px 0'}" />
        <Card>
          <p slot="title">
            <Icon type="ios-stats" size="24"></Icon>&nbsp;服务节点信息
          </p>
          <Row>
            <Col span="8">
              <span>模板类型: </span>
              <span class="node_desc">{{ tpl_type }}</span>
            </Col>
            <Col span="8">
              <span>OP负责人: </span>
              <span class="node_desc">{{ op_manager }}</span>
            </Col>
            <Col span="8">
              <span>RD负责人: </span>
              <span class="node_desc">{{ rd_manager }}</span>
            </Col>
          </Row>
        </Card>
        <Card :style="{margin: '25px 0 10px 0'}" v-if="instance_card">
          <p slot="title">
            <Icon type="ios-card" size="24"></Icon>&nbsp;节点实例信息
          </p>
          <Row :style="{margin: '-5px 0 5px'}">
            <Col span="8">
            <Button icon="ios-add-circle-outline" :style="{color: '#87b87f'}" @click="show_instance_dlg">机器信息</Button>
            <Button icon="ios-cloud-circle-outline" :style="{color: '#87b87f'}">元信息</Button>
            </Col>
            <Col span="4" offset="12">
              <Input placeholder="Enter text" style="width: 100%">
                <Icon type="ios-search" slot="suffix" />
              </Input>
            </Col>
          </Row>
          <Table border :columns="columns" :data="instances">
            <template slot-scope="{ row, index }" slot="action">
              <Button type="primary" size="small" style="margin-right: 5px" @click="instance_edit(index)">编辑</Button>
              <Button type="error" size="small" @click="instance_remove(index)">删除</Button>
            </template>
            <template slot-scope="{ row, index }" slot="instance_status">
							<i-switch size="large" v-model="row.status">
								<span slot="open">在线</span>
								<span slot="close">下线</span>
							</i-switch>
            </template>
          </Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
              <Page :total="instance_total" :current="1" @on-change="change_page"></Page>
            </div>
          </div>
        </Card>
      </div>
    </Split>

    <!-- NOTE(服务树右键菜单相关操作) -->
    <div id="right_menu" v-bind:style="show_menu_style">
      <ul>
        <li v-if="show_add" @click="add_node"><Icon type="ios-add-circle-outline" /> 节点添加</li>
        <li v-if="show_del" @click="del_node"><Icon type="ios-remove-circle-outline" /> 节点删除</li>
        <li v-if="show_ren" @click="ren_node"><Icon type="ios-contrast" /> 节点改名</li>
      </ul>
    </div>

    <!-- NOTE(服务树右键菜单对话框) -->
    <Modal v-model="add_node_dlg" :closable="false" width="560" @on-ok="do_add_node" @on-cancel="cancel">
      <p slot="header" style="text-align:center">
        <Icon type="ios-add-circle-outline"></Icon>
        <span>节点添加表单</span>
      </p>
      <Form :model="formItem" :label-width="80">
        <FormItem label="节点模板">
					<Select v-model="tpl">
						<Option v-for="item in tpl_list" :value="item" :key="item">{{ item }}</Option>
					</Select>
        </FormItem>
        <FormItem label="节点类型">
          <RadioGroup v-model="formItem.node_type">
            <Radio label="directory"><span>目录节点</span></Radio>
            <Radio label="leaf"><span>叶子节点</span></Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="节点名称">
          <Input v-model="formItem.add_node_name" placeholder="节点名称, 不能包含非法字符."></Input>
        </FormItem>
        <FormItem label="rd负责人">
          <Input v-model="formItem.rd_manager" placeholder="请输入rd负责人."></Input>
        </FormItem>
        <FormItem label="op负责人">
          <Input v-model="formItem.op_manager" placeholder="请输入op负责人."></Input>
        </FormItem>
      </Form>
    </Modal>
    <Modal v-model="del_node_dlg" :closable="false" width="360" @on-ok="do_del_node" @on-cancel="cancel">
      <p slot="header" style="color:#f60; text-align:center">
        <Icon type="ios-information-circle"></Icon>
        <span>节点删除确认</span>
      </p>
      <div>
        <strong style="color:#f60;">请慎重确认要删除该节点吗?</strong>
      </div>
    </Modal>
    <Modal v-model="ren_node_dlg" :closable="false" width="560" @on-ok="do_ren_node" @on-cancel="cancel">
      <p slot="header" style="text-align:center">
        <Icon type="ios-contrast"></Icon>
        <span>节点修改表单</span>
      </p>
      <Form :model="formItem" :label-width="80">
        <FormItem label="节点路径">
          <strong>{{ tip_node }}</strong>
        </FormItem>
        <FormItem label="节点名称">
          <Input v-model="formItem.new_node_name" placeholder="节点名称, 不能包含非法字符."></Input>
        </FormItem>
      </Form>
    </Modal>

    <!-- 实例信息对话框相关操作 -->
    <Modal v-model="instance_dlg" :closable="false" width="560" @on-ok="do_add_instance" @on-cancel="cancel">
      <p slot="header" style="text-align:center">
        <Icon type="ios-apps"></Icon>
        <span>节点实例表单</span>
      </p>
      <Form :model="formItem" :label-width="80">
        <FormItem label="节点名称">
        <Input v-model="formItem.new_instance" type="textarea" :autosize="{minRows: 4}" placeholder="实例名称, 一行一个IP."></Input>
        </FormItem>
      </Form>
    </Modal>

  </div>
</template>

<script>
import 'jquery'
import 'ztree'
import 'ztree/css/metroStyle/metroStyle.css'
import axios from 'axios'
import qs from 'qs'
import expandRow from '@/components/index/SInfo'

export default {
  name: 'STree',
  data() {
    return {
      split_rate: 0.2,
      tree_nodes: null,
      tip_node: null,
      ztree_obj: null,
      show_menu_style: null,
      tpl: '默认模板',
      tpl_list: null,
      show_add: true,
      show_del: true,
      show_ren: true,
      add_node_dlg: false,
      del_node_dlg: false,
      ren_node_dlg: false,
      lucene: null,
      search_match_nodes: [],
      instance_card: false,
      formItem: {
        node_type: 'leaf',
        add_node_name: null,
        op_manager: null,
        rd_manager: null,
        new_node_name: null,
        new_instance: null
      },
      columns: [
      ],
      instances: [
      ],
      instance_total: 0,
      instance_dlg: false,
      tpl_type: null,
      op_manager: null,
      rd_manager: null,
      setting: {
        view: {
          showLine: true,
          dblClickExpand: false,
          selectedMulti: false,
          showTitle: false,
          showIcon: true,
          fontCss: this.font_css
        },
        data: {
          simpleData: {
            enable: true,
            idKey: 'id',
            pIdKey: 'pid',
            rootPId: ''
          }
        },
        callback: {
          onClick: this.ztree_click,
          onRightClick: this.ztree_right_click
        }
      }
    }
  },
  methods: {
    load_tree() {
      let url = 'http://localhost:5000/stree/api/v1/load/tree';
      axios.get(url).then((res) => {
        let r = res.data;
        if (r.code != 0) {
          this.$Message.error(r.msg);
          return;
        }
        this.tree_nodes = r.data.tree_list;
        this.tip_node = r.data.expand_node;

        $.fn.zTree.init($('#service_tree'), this.setting, this.tree_nodes);
        this.ztree_obj = $.fn.zTree.getZTreeObj('service_tree');
        this.ztree_obj.selectNode(this.ztree_obj.getNodeByParam('id', this.tip_node, null));

        // NOTE(更新search_match_nodes)
        console.log(this.search_match_nodes);
        if (this.search_match_nodes && this.search_match_nodes.length > 0) {
          this.search_match_nodes = [];
          this.search_match_nodes.push(this.ztree_obj.getNodeByParam('id', this.tip_node, null));
        }
        this.load_node_info();
      }, (res) => {
        this.$Message.error('请求/load/tree接口失败!');
      });
    },
    load_tpl() {
      let url = 'http://localhost:5000/stree/api/v1/load/tpl';
      axios.get(url).then((res) => {
        let r = res.data;
        if (r.code != 0) {
          this.$Message.error(r.msg);
          return;
        }
        this.tpl_list = r.data;
      }, (res) => {
        this.$Message.error('请求/load/tpl接口失败!');
      });
    },
    font_css(tree_id, node_obj) {
      if (!!node_obj.highlight) {
        return {color: '#428BCA', 'font-weight': 'bold'};
      }
      return {color: '#333', 'font-weight': 'normal'}
    },
    ztree_click(event, tree_id, node_obj) {
      let tip_node = node_obj.id;
      this.tip_node = tip_node;
      if (node_obj.isParent == false) {
        this.instance_card = true;
        this.load_instance(0);
      } else {
        this.instance_card = false;
      }
      this.highlight_nodes(false);
      this.load_node_info();
    },
    ztree_right_click(event, tree_id, node_obj) {
      if (node_obj.pid == '') {
        // NOTE(根节点)
        this.show_del = false;
        this.show_ren = false;
      } else if (node_obj.name == 'backpool') {
        // NOTE(backpool)
        this.show_add = false;
        this.show_del = false;
        this.show_ren = false;
        return;
      } else {
        this.show_add = true;
        this.show_del = true;
        this.show_ren = true;
      }
      this.ztree_obj.selectNode(node_obj);  
      let tip_node = node_obj.id;
      this.tip_node = tip_node;
      this.show_menu_style = {
        top: event.clientY + 5 + 'px',
        left: event.clientX + 'px',
        visibility: 'visible',
        'z-index': 1
      }
    },
    hide_menu() {
      this.show_menu_style = {visibility: 'hidden'};
    },
    mouse_down(e) {
      // NOTE(注: 当点击菜单时, $(e.target).parents('#right_menu').length 大于 1)
      if (!(e.target.id == 'right_menu' || $(e.target).parents('#right_menu').length>0)) {
        this.hide_menu();
      }
    },
    add_node(e) {
      this.hide_menu();
      this.add_node_dlg = true;
    },
    do_add_node() {
      let tip_node_obj = this.ztree_obj.getSelectedNodes()[0];
      let tip_node_id = tip_node_obj.id;
      let tip_node_pid = tip_node_obj.pid
      let tip_node_name = tip_node_obj.name;
			let is_leaf = 1
      let is_parent = false;
      if (this.formItem.node_type == 'directory') {
          is_parent = true;
          is_leaf = 0;
      }
      let new_name = this.formItem.add_node_name;
      let url = 'http://localhost:5000/stree/api/v1/add/node';
      let post_data = qs.stringify({
				tpl: this.tpl,
        leaf: is_leaf,
        pnode: tip_node_id,
        new_node: new_name,
        op: this.formItem.op_manager,
        rd: this.formItem.rd_manager
      });
			console.log(post_data);
      axios.post(url, post_data).then((res) => {
        let r = res.data;
        if (r.code != 0) {
          this.$Message.warning(r.msg);
          return;
        }
        let new_node = {
          id: tip_node_id + '.' + new_name,
          pid: tip_node_id,
          name: new_name,
          isParent: is_parent
        };
        this.ztree_obj.addNodes(tip_node_obj, new_node);
        this.formItem.node_type = 'leaf';
        this.formItem.add_node_name = null;
      }, (res) => {
        this.$Message.error('请求/load/tree接口失败!');
      });
    },
    cancel() {
    },
    del_node(e) {
      this.hide_menu();
      this.del_node_dlg = true;
    },
    do_del_node() {
      let nodes = this.ztree_obj.getSelectedNodes();
      if (nodes && nodes.length > 0) {
        if (nodes[0].children && nodes[0].children.length > 0) {
          this.$Message.warning('该节点为父节点, 不能进行删除!');
        } else {
          let node_obj = nodes[0];
          let post_data = qs.stringify({
            node: node_obj.id
          });
          console.log(post_data);
          this.ztree_obj.removeNode(node_obj);
        }
      }
    },
    ren_node(e) {
      this.hide_menu();
      this.ren_node_dlg = true;
    },
    do_ren_node() {
      let tip_node_obj = this.ztree_obj.getSelectedNodes()[0];
      let tip_node_id = tip_node_obj.id;
      let tip_node_pid = tip_node_obj.pid;
      let tip_node_name = tip_node_obj.name;
      if (tip_node_obj) {
        tip_node_obj.name = this.formItem.new_node_name;
        this.ztree_obj.updateNode(tip_node_obj);

        this.tip_node = tip_node_pid + '.' + this.formItem.new_node_name
        this.formItem.new_node_name = null;
      }
    },
    global_search() {
      let url = 'http://localhost:5000/stree/api/v1/query';
      let post_data = qs.stringify({
        lucene: this.lucene
      });
      axios.post(url, post_data).then((res) => {
        let search_nodes = res.data.data;
        // NOTE(展开节点)
        this.search_match_nodes = [];
        for (let expand_node of search_nodes) {
          let node = this.ztree_obj.getNodeByParam('id', expand_node);
          if (node == null) {
            this.search_match_nodes = [];
          } else {
            this.ztree_obj.selectNode(node);
            this.search_match_nodes.push(node);
          }
        }
        // NOTE(节点信息、实例信息, 默认显示第一个节点)
        if (this.search_match_nodes.length != 0) {
          let default_node = this.search_match_nodes[0].id;
          let is_parent = this.search_match_nodes[0].isParent;
          this.tip_node = default_node;
          this.load_node_info();
          if (!is_parent) {
            this.instance_card = true;
            this.load_instance(0);
          }
        }
        // NOTE(高亮选中节点)
        this.highlight_nodes(true);
      }, (res) => {
        this.$Message.error('请求/query接口失败!');
      });
    },
    highlight_nodes(is_highlight) {
      for (let node of this.search_match_nodes) {
        node.highlight = is_highlight;
        this.ztree_obj.updateNode(node);
      }
    },
    instance_edit(index) {
      let name = this.instances[index].name;
      console.log(name);
    },
    instance_remove(index) {
      let name = this.instances[index].name;
      console.log(name);
    },
    change_page(index) {
      let offset = (index - 1) * 10;
      this.load_instance(offset);
    },
    load_instance(offset) {
      this.columns = [
        {
          type: 'expand', width: 50,
          render: (h, params) => {
            return h(expandRow, {
              props: {
                row: params.row
              }
            })
          }
        },
        {title: '主机名', key: 'hostname', sortable: true},
        {title: 'IP地址', key: 'ip', sortable: true},
        {title: '服役状态', key: 'status', width: 150, slot: 'instance_status'},
        {title: '部署分组', key: 'deploy', width: 150},
        {title: '定时任务', key: 'crontab', width: 150},
        {title: '操作', key: 'operation', width: 150, slot: 'action'}
      ];
      let post_data = qs.stringify({
        node: this.tip_node,
        offset: offset
      });
      let url = 'http://localhost:5000/stree/api/v1/load/instance';
      axios.post(url, post_data).then((res) => {
        this.instances = res.data.data.instances;
        this.instance_total = res.data.data.total;
      }, (res) => {
        this.$Message.error('请求/load/instance接口失败!');
      });
    },
    load_node_info() {
      let url = 'http://localhost:5000/stree/api/v1/load/node/info';
      let post_data = qs.stringify({
        node: this.tip_node
      });
      axios.post(url, post_data).then((res) => {
        this.tpl_type = res.data.data.tpl;
        this.op_manager = res.data.data.op;
        this.rd_manager = res.data.data.rd;
      }, (res) => {
        this.$Message.error('请求/load/node/info接口失败!');
      });
    },
    show_instance_dlg() {
      this.instance_dlg = true;
    },
    do_add_instance() {
      let post_data = qs.stringify({
        node: this.tip_node,
        ips: this.formItem.new_instance
      });
      let url = 'http://localhost:5000/stree/api/v1/add/instance';
      axios.post(url, post_data).then((res) => {
        this.load_instance(0);
      }, (res) => {
        this.$Message.error('请求/add/instance接口失败!');
      });
    }
  },
  mounted() { 
    this.load_tree();
    this.load_tpl();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stree{
  height: 640px;
  border: 1px solid #dcdee2;
}
.split-pane{
  padding: 6px;
  height: 630px;
  overflow: auto;
}
.split-right-pane{
  padding: 0 15px;
  height: 630px;
  overflow: auto;
}
.ztree {
  margin: 0;
  padding: 8px 0 0 0px;
  margin-left: -3px;
  color: #333;
}
/* 右键菜单样式 */
div#right_menu{
  position: fixed;
  visibility: hidden;
  top: 0;
  text-align: left;
  padding: 2px;
  box-sizing: content-box;
  width: 100px;
  -webkit-box-shadow: rgba(0, 0, 0, 0.2) 0 2px 4px;
  box-shadow: rgba(0, 0, 0, 0.2) 0 2px 4px;
  background-color: rgb(255, 255, 255);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-image-source: initial;
  border-image-slice: initial;
  border-image-width: initial;
  border-image-outset: initial;
  border-image-repeat: initial;
}
div#right_menu ul{
  margin: 0px;
  padding: 0px
}
div#right_menu ul li{
  margin: 0px;
  padding: 2px 10px;
  cursor: pointer;
  color: rgb(68, 68, 68);
  font-weight: 500;
  font-size: 13px;
  font-family: "Open Sans";
  list-style: none outside none;
  background-color: rgb(255, 255, 255);
}
div#right_menu ul li:hover{
  color: white;
  background-color: #428BCA;
}
.node_desc{
  font: bold 15px arial,sans-serif;
  color: #438eb9;
}
</style>
