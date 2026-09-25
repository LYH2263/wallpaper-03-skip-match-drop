<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([]); const busy = ref(false)
onMounted(async () => { items.value = (await getJSON('/api/rolls')).items })
async function setMatch(r, m) {
  if (busy.value || r.match_type === m) return
  busy.value = true
  try {
    const updated = await patchJSON(`/api/rolls/${r.id}`, { match_type: m })
    const i = items.value.findIndex(x => x.id === r.id)
    if (i >= 0) items.value[i] = updated
  } finally { busy.value = false }
}
</script>
<template>
  <div class="page"><h1>纸卷规格</h1>
  <div v-for="r in items" :key="r.id" class="roll-chip">
    {{ r.name }} · 宽{{ r.width }} · 长{{ r.length }} · 花距{{ r.pattern_cm }}cm
    <span class="match-toggle">
      默认匹配：
      <button :class="{ active: (r.match_type || 'straight') === 'straight' }" @click="setMatch(r, 'straight')">直对</button>
      <button :class="{ active: r.match_type === 'offset' }" @click="setMatch(r, 'offset')">跳对</button>
    </span>
    <p v-if="r.data_quality === 'dirty'" class="warn">{{ r.note }}</p>
  </div>
  <p class="hint">修改默认匹配只影响之后的新测算，不会改写已保存的记录。</p>
  </div>
</template>
