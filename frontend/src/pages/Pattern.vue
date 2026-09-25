<template>
  <div class="page"><h1>对花说明</h1>
  <p>有花距时在墙高上加花高（pattern_cm/100）作为每条长度，再算每卷可裁条数。</p>
  <p><strong>直对</strong>：drop_len = 层高 + 花高。</p>
  <p><strong>跳对</strong>：在层高基础上再加半个花高，半花高向上取到毫米后换算，再算每卷条数与卷数；花高为负时拒绝测算。</p>
  <p>花高为 0 时，直对与跳对结果相同。每次保存会把当次匹配方式、drop_len 与卷数一并钉住，事后修改卷材默认匹配不会改写旧记录。</p></div>
</template>
