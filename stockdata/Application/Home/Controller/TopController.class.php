<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class TopController extends Controller {
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
    }

    public function __call($name, $arguments) {
        $count = M($name)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M($name)->order('id desc')->limit($page->firstRow.','.$page->listRows)->select();

        $this->assign('list', $list);
        $this->assign('today', $this->today);
        $this->assign('page', $show);

        $this->display("Top:$name");
    }
}