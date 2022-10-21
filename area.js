
var levelDic = { 1: 'province', 2: 'city', 3: 'county', 4: 'town', 5: 'village' }

function setNextArea(i,code) {
  console.info(i + "-" + code);
    //return;

    //area[0].options.length = 0;//先清空
    if (dicID[code]) {
        
    var area = $("#" + levelDic[i]);
    dicID[code].forEach(function (value, index, obj) {
        area[0].add(new Option(dicName[value], value));
    });
    }
}
$(function () {
    for (var k in levelDic) {
        if (k==5) break;
        console.info('#' + levelDic[k] + "-" + k);
        $('#' + levelDic[k]).change({ a:parseInt(k)+1}, function(e) {
            setNextArea(e.data.a, $(this).val());
            //console.info(k + "-" + levelDic[k]);
        });
    }

    setNextArea(1, 0);
});