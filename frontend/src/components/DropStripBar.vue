<script setup>
defineProps({ drops: Number, dropLen: Number, rolls: Number, match: String })
const matchLabel = m => (m === 'offset' ? '跳对' : '直对')
</script>
<template>
  <div class="strip-bar">
    <details>
      <summary>展开示意（共 {{ drops }} 条，约 {{ rolls }} 卷）</summary>
      <p class="drop-len">当次每条长 drop_len = <strong>{{ dropLen }} m</strong>（{{ matchLabel(match) }}）</p>
      <div class="strip-row">
        <div v-for="n in Math.min(drops || 0, 24)" :key="n" class="strip" :style="{ height: `${Math.min(120, (dropLen || 2) * 30)}px` }"></div>
      </div>
    </details>
  </div>
</template>
