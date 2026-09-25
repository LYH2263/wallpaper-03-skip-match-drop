<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1)
const match = ref('straight'); const out = ref(null); const err = ref('')
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality === 'clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality === 'clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) { rollId.value = rolls.value[0].id; match.value = rolls.value[0].match_type || 'straight' }
})
// 切换卷材时，匹配方式跟随卷材默认；用户仍可在本次测算中手动切换
watch(rollId, id => {
  const r = rolls.value.find(x => x.id === id)
  if (r) match.value = r.match_type || 'straight'
})
async function run(save) {
  err.value = ''; out.value = null
  try {
    out.value = save
      ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, match: match.value, save: true })
      : await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}&match=${match.value}`)
  } catch (e) { err.value = e.message }
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <label class="match-toggle"><input type="radio" value="straight" v-model="match" />直对</label>
  <label class="match-toggle"><input type="radio" value="offset" v-model="match" />跳对</label>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <p v-if="err" class="warn">已拒绝测算：{{ err }}</p>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m（{{ out.match === 'offset' ? '跳对' : '直对' }}）
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" :match="out.match" /></div>
  </div>
</template>
