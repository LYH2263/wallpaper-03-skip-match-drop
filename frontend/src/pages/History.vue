<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const runNo = ref(''); const detail = ref(null); const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
const matchLabel = m => (m === 'offset' ? '跳对' : '直对')
async function lookBack() {
  err.value = ''; detail.value = null
  if (!String(runNo.value).trim()) return
  try {
    detail.value = await getJSON(`/api/runs/${String(runNo.value).trim()}`)
  } catch (e) { err.value = e.message }
}
</script>
<template>
  <div class="page"><h1>记录</h1>
  <div class="lookup">
    <label>按编号回看：<input v-model="runNo" type="number" min="1" @keyup.enter="lookBack" /></label>
    <button @click="lookBack">回看</button>
  </div>
  <div v-if="err" class="warn">查无此记录：{{ err }}</div>
  <div v-if="detail" class="run-detail">
    <strong>#{{ detail.id }}</strong> {{ detail.wall_name }} → {{ detail.result?.rolls }} 卷
    · {{ detail.result?.drops }} 条 · 每条 {{ detail.result?.drop_len_m }}m
    · {{ matchLabel(detail.result?.match) }}
    <p class="hint">匹配方式以写入时为准（{{ matchLabel(detail.result?.match) }}），不受卷材当前默认影响。</p>
  </div>
  <ul>
    <li v-for="r in items" :key="r.id">
      #{{ r.id }} {{ r.wall_name }} → {{ r.result?.rolls }} 卷 · 每条 {{ r.result?.drop_len_m }}m · {{ matchLabel(r.result?.match) }}
    </li>
  </ul></div>
</template>
