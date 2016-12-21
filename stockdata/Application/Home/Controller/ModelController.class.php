<?php
namespace Home\Controller;
use Think\Controller;

defined('PAGE_COUNT') or define('PAGE_COUNT', 50);

class ModelController extends Controller {
    private $focusType;
    private $today;

    protected function _initialize() {
        $this->today = C('TODAY');
        $this->focusType = array(
            'volumeBreak5d' => 2,
            'eneUpper' => 3,
            'eneLower' => 4,
            'closeEneLower' => 5,
            'volumeBreak20d' => 6
        );
    }

    public function volumeBreak5d() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['volumeBreak5d'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->join('left join volume_break on focus_pool.code = volume_break.code and focus_pool.date = volume_break.date')
            ->join('left join super_wave on focus_pool.code = super_wave.code')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,latest,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,v2ma5,v2ma20,percent,cur_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,count,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:volumeBreak5d');
    }

    public function volumeBreak20d() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['volumeBreak20d'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->join('left join volume_break on focus_pool.code = volume_break.code and focus_pool.date = volume_break.date')
            ->join('left join super_wave on focus_pool.code = super_wave.code')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,latest,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,v2ma5,v2ma20,percent,cur_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,count,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:volumeBreak20d');
    }

    public function eneUpper() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['eneUpper'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,latest,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,count,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:eneUpper');
    }

    public function eneLower() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['eneLower'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,latest,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,count,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:eneLower');
    }

    public function closeEneLower() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['closeEneLower'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'dist_per' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join('left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date')
            ->join('left join close_ene_lower on focus_pool.code = close_ene_lower.code and focus_pool.date = close_ene_lower.date')
            ->join('left join stocks_info on focus_pool.code = stocks_info.code')
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,latest,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,dist_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,count,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:closeEneLower');
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