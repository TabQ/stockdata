<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class IndexController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
    }

    public function __call($name, $arguments) {
        $params = I('get.');
        extract($params);

        !empty($type_id) && $map['type_id'] = $type_id;
        !empty($subtype_id) && $map['subtype_id'] = $subtype_id;

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $sort = $name == 'index' ? 'yield_rate desc' : ($desc == 1 ? "$name desc" : "$name");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join focus_type on focus_pool.type_id = focus_type.id')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->field('focus_pool.id, focus_pool.code, focus_pool.date, count, latest, industry, focus_pool.man_date, focus_type.name as fname, subtype_id, focus_pool.cost_price, focus_pool.yield_rate, stocks_info.name, rec3minus, rec5minus, rec3tops, rec5tops, timetomarket')
            ->order($sort)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $typeList = M('focus_type')->order('id')->select();

        $this->assign('type_list', $typeList);
        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Index:index');
    }

    public function delete() {
        $map['id'] = array('IN', I('get.ids'));

        $result = M('focus_pool')->where($map)->delete();

        if($result) {
            $this->success('操作成功！');
        } else {
            $this->error('操作失败！');
        }
    }
}