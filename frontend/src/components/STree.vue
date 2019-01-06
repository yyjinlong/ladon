<template>
  <div class="stree" @mousedown="mouse_down($event)">
    <Split v-model="split_rate" min="285px">
      <div slot="left" class="split-pane">
        <Input search placeholder='支持lucene语法, 如: host: "app10"' />
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
              <span>服务类型: </span>
              <span class="node_desc">{{ service_type }}</span>
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
        <Card :style="{margin: '25px 0 0 0'}">
          <p slot="title">
            <Icon type="ios-card" size="24"></Icon>&nbsp;节点实例信息
          </p>
          <Row :style="{margin: '-5px 0 5px'}">
            <Col span="8">
            <Button icon="ios-add-circle-outline" :style="{color: '#87b87f'}">机器信息</Button>
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
          </Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
            	<Page :total="100" :current="1" @on-change="changePage"></Page>
            </div>
          </div>
        </Card>
      </div>
    </Split>

    <!-- NOTE(服务树右键菜单相关操作) -->
    <div id="right_menu" v-bind:style="show_menu_style">
      <ul>
        <li id="add_node" @click="add_node"><Icon type="ios-add-circle-outline" /> 节点添加</li>
        <li id="del_node" @click="del_node"><Icon type="ios-remove-circle-outline" /> 节点删除</li>
        <li id="ren_node" @click="ren_node"><Icon type="ios-contrast" /> 节点改名</li>
      </ul>
    </div>

    <Modal v-model="add_node_dlg" :closable="false" width="560" @on-ok="do_add_node" @on-cancel="cancel">
      <p slot="header" style="text-align:center">
        <Icon type="ios-add-circle-outline"></Icon>
        <span>节点添加表单</span>
      </p>
      <Form :model="formItem" :label-width="80">
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

    <!-- 实例信息相关操作 -->

  </div>
</template>

<script>
import 'jquery'
import 'ztree'
import 'ztree/css/metroStyle/metroStyle.css'
import axios from 'axios'
import expandRow from '@/components/SInfo'

export default {
  name: 'STree',
  data() {
    return {
      split_rate: 0.2,
      tree_nodes: null,
      tip_node: null,
      ztree_obj: null,
      show_menu_style: null,
      add_node_dlg: false,
      del_node_dlg: false,
      ren_node_dlg: false,
      formItem: {
        node_type: 'leaf',
        add_node_name: null,
        op_manager: null,
        rd_manager: null,
        new_node_name: null
      },
      columns: [
      ],
      instances: [
      ],
      service_type: null,
      op_manager: null,
      rd_manager: null,
      setting: {
        view: {
          showLine: true,
          dblClickExpand: false,
          selectedMulti: false
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
    ztree_click(event, tree_id, node_obj) {
      let tip_node = node_obj.id;
      this.tip_node = tip_node;
    },
    ztree_right_click(event, tree_id, node_obj) {
      if (node_obj.pid == '') {
        return;
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
      let is_parent = false;
      if (this.formItem.node_type == 'directory') {
        is_parent = true;
      }
      let new_name = this.formItem.add_node_name;
      let new_node = {id: tip_node_id + 'test', pid: tip_node_id, name: new_name, isParent: is_parent};
      this.ztree_obj.addNodes(tip_node_obj, new_node);
      this.formItem.node_type = 'leaf';
      this.formItem.add_node_name = null;
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
          this.ztree_obj.removeNode(nodes[0]);
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
    instance_edit(index) {
      let name = this.instances[index].name;
      console.log(name);
    },
    instance_remove(index) {
      let name = this.instances[index].name;
      console.log(name);
    },
    changePage(index) {
      console.log(index);
    }
  },
  mounted() {
    draw_tree(this);
    load_instances(this);
  }
}

function load_instances(_this) {
  _this.columns = [
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
    {title: '名字', key: 'name', sortable: true},
    {title: '年龄', key: 'age', sortable: true},
    {title: '操作', key: 'action', width: 150, slot: 'action'}
  ];
  let url = 'http://localhost:5000/list';
  axios.get(url).then((res) => {
    _this.instances = res.data;
  }, (res) => {
    console.log('Request table list intf error.');
  });
}

function draw_tree(_this) {
  let root = 'com';
  let tree_nodes = [
    {id:root, pid:root, name:root},
    {id:'com.card', pid:root, name:'card'}, 
    {id:'com.card.app1', pid:'com.card', name:'app1'}, 
    {id:'com.credit', pid:root, name:'credit'}, 
    {id:'com.credit.bbs', pid:'com.credit', name:'bbs'}, 
    {id:'com.credit.pay', pid:'com.credit', name:'pay'}, 
  ];
  _this.tree_nodes = tree_nodes;
  _this.tip_node = root;
  let expand_node = 'com.card';

  $.fn.zTree.init($('#service_tree'), _this.setting, _this.tree_nodes);
  _this.ztree_obj = $.fn.zTree.getZTreeObj('service_tree');
  _this.ztree_obj.selectNode(_this.ztree_obj.getNodeByParam('id', expand_node, null));
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stree{
  height: 750px;
  border: 1px solid #dcdee2;
}
.split-pane{
  padding: 6px;
}
.split-right-pane{
  padding: 0 15px;
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
