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
            'eneUpper' => 2,
            'eneLower' => 3,
            'closeEneLower' => 4,
            'volBreak5d' => 5,
            'volBreak10d' => 6,
            'volBreak20d' => 7,
            'volShrinkMax' => 8,
            'volShrinkMax5d' => 9,
            'volShrinkMax10d' => 10,
            'volShrinkMax20d' => 11,
            'volShrinkMax60d' => 12,
            'volShrinkMax120d' => 13,
            'volShrinkMa5d' => 14,
            'volShrinkMa10d' => 15,
            'volShrinkMa20d' => 16,
            'volShrinkMa60d' => 17,
            'volShrinkMa120d' => 18,
        );
    }

    public function volumeShrink() {
        $params = I('get.');
        extract($params);

        if(empty($date) || $date == 'latest') {
            $lastData = M('volume')->field('date')->order('date desc')->limit(1)->find();
            $lastDay = $lastData['date'];

            $map['volume.date'] = array('eq', $lastDay);
        }

        $count = M('volume')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'vol_shrink_max' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('volume')
            ->where($map)
            ->join("left join stocks_extends on volume.code = stocks_extends.code and volume.date = stocks_extends.date and stocks_extends.type='S'")
            ->join("left join stocks_info on volume.code = stocks_info.code and stocks_info.type='S'")
            ->field('volume.code, volume.date, name, p_change, vol_shrink_max, vol_shrink_max_5d, vol_shrink_max_10d, vol_shrink_max_20d, vol_shrink_max_60d, vol_shrink_max_120d,
            vol_shrink_ma_5d, vol_shrink_ma_10d, vol_shrink_ma_20d, vol_shrink_ma_60d, vol_shrink_ma_120d')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:volumeShrink');
    }

    public function volumeBreak5d() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['volBreak5d'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join("left join stocks_extends on focus_pool.code = stocks_extends.code and focus_pool.date = stocks_extends.date and stocks_extends.type='S'")
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join('left join volume on focus_pool.code = volume.code and focus_pool.date = volume.date')
            ->join('left join super_wave on focus_pool.code = super_wave.code')
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,vol_break_5d,vol_break_10d,vol_break_20d,p_change,percent,cur_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:volumeBreak5d');
    }

    public function volumeBreak10d() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['volBreak10d'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join("left join stocks_extends on focus_pool.code = stocks_extends.code and focus_pool.date = stocks_extends.date and stocks_extends.type='S'")
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join('left join volume on focus_pool.code = volume.code and focus_pool.date = volume.date')
            ->join('left join super_wave on focus_pool.code = super_wave.code')
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,vol_break_5d,vol_break_10d,vol_break_20d,p_change,percent,cur_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
            ->order($order)
            ->limit($page->firstRow.','.$page->listRows)
            ->select();

        $this->assign('today', $this->today);
        $this->assign('list', $list);
        $this->assign('page', $show);

        $this->display('Model:volumeBreak10d');
    }

    public function volumeBreak20d() {
        $params = I('get.');
        extract($params);

        $map['type_id'] = $this->focusType['volBreak20d'];

        $count = M('focus_pool')->where($map)->count();
        $page = new \Think\Page($count, PAGE_COUNT);
        $show = $page->show();

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join("left join stocks_extends on focus_pool.code = stocks_extends.code and focus_pool.date = stocks_extends.date and stocks_extends.type='S'")
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join('left join volume on focus_pool.code = volume.code and focus_pool.date = volume.date')
            ->join('left join super_wave on focus_pool.code = super_wave.code')
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,vol_break_5d,vol_break_10d,vol_break_20d,p_change,percent,cur_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
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
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
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
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
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

        $order = !isset($sort) ? 'date desc' : ($desc == 1 ? "$sort desc" : "$sort");

        $list = M('focus_pool')
            ->where($map)
            ->join("left join k_data on focus_pool.code = k_data.code and focus_pool.date = k_data.date and k_data.type='S'")
            ->join("left join stocks_extends on focus_pool.code = stocks_extends.code and focus_pool.date = stocks_extends.date and stocks_extends.type='S'")
            ->join("left join stocks_info on focus_pool.code = stocks_info.code and stocks_info.type='S'")
            ->join('left join stocks_report on focus_pool.code = stocks_report.code')
            ->join('left join stocks_growth on focus_pool.code = stocks_growth.code')
            ->field('focus_pool.id,name,focus_pool.date,focus_pool.code,focus_pool.man_date,focus_pool.cost_price,dist_per,stocks_info.bvps,pe,profits_yoy,mbrg,close,timetomarket,focus_pool.yield_rate')
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