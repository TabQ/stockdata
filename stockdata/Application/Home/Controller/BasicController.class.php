<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class BasicController extends Controller {
    public function __call($name, $arguments) {
        if ($name == 'breakAssets' || $name == 'lowMinusAssetRate') {
            exit;
        }

        $params = I('get.');
        extract($params);

        $map['stocks_info.pe'] = array('gt', 0);

        $count = M('stocks_info')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $lastData = M('k_data')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];

        $sort = $name == 'info' ? 'pe' : ($desc == 1 ? "$name desc" : "$name");

        $list = M('stocks_info')
            ->where($map)
            ->join("left join k_data on stocks_info.code = k_data.code and date='$lastDay'")
            ->join('left join stocks_report on stocks_info.code = stocks_report.code')
            ->join('left join stocks_growth on stocks_info.code = stocks_growth.code')
            ->field('pe, name, stocks_info.code, industry, close, stocks_info.bvps, profits_yoy, mbrg, outstanding, timetomarket')
            ->order($sort)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Basic:info');
    }

    public function breakAssets() {
        $lastData = M('k_data')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];

        $map['date'] = array('eq', $lastDay);

        $map['stocks_info.type'] = 'S';

        $count = M('stocks_info')
            ->where($map)
            ->join('k_data on k_data.code = stocks_info.code')
            ->where('low <= stocks_info.bvps')->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('stocks_info')
            ->where($map)
            ->join('k_data on k_data.code = stocks_info.code')
            ->where('low <= stocks_info.bvps')
            ->join('left join stocks_report on stocks_info.code = stocks_report.code')
            ->join('left join stocks_growth on stocks_info.code = stocks_growth.code')
            ->field('name, stocks_info.code, industry, low, stocks_info.bvps, pe, profits_yoy, mbrg, timetomarket')
            ->order('profits_yoy desc')
            ->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Basic:breakAssets');
    }

    public function lowMinusAssetRate() {
        $lastData = M('k_data')->field('date')->order('date desc')->limit(1)->find();
        $lastDay = $lastData['date'];

        $map['date'] = array('eq', $lastDay);

        $map['stocks_info.type'] = 'S';

        $count = M('stocks_info')
            ->where($map)
            ->join('k_data on k_data.code = stocks_info.code')
            ->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $list = M('stocks_info')
            ->where($map)
            ->join('k_data on k_data.code = stocks_info.code')
            ->join('left join stocks_report on stocks_info.code = stocks_report.code')
            ->join('left join stocks_growth on stocks_info.code = stocks_growth.code')
            ->field('name, stocks_info.code, industry, (low-stocks_info.bvps)/stocks_info.bvps as lmar, low, stocks_info.bvps, pe, profits_yoy, mbrg, timetomarket')
            ->order('lmar')
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Basic:lowMinusAssetRate');
    }
}

