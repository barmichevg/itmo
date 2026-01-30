<script setup>
const props = defineProps({
  hits: { type: Array, required: true },
  activeId: { type: [Number, String, null], default: null }
})

const emit = defineEmits(['view'])

function fmtTime(iso) {
  try { return new Date(iso).toLocaleString() } catch { return iso }
}

function isActive(h) {
  return props.activeId != null && String(h.id) === String(props.activeId)
}
</script>

<template>
  <div class="tableWrap">
    <table>
      <thead>
      <tr>
        <th style="width: 70px;">Действие</th>
        <th style="width: 90px;">X</th>
        <th style="width: 90px;">Y</th>
        <th style="width: 90px;">R</th>
        <th style="width: 120px;">Результат</th>
        <th style="width: 220px;">Время</th>
        <th style="width: 120px;">μs</th>
      </tr>
      </thead>

      <tbody>
      <tr
          v-for="h in hits"
          :key="h.id"
          :class="{ 'active-row': isActive(h) }"
      >
        <td>
          <button class="button btnSmall" type="button" @click="emit('view', h)">▶</button>
        </td>

        <td>{{ h.x }}</td>
        <td>{{ h.y }}</td>
        <td>{{ h.r }}</td>

        <td>
            <span class="badge" :class="h.hit ? 'ok' : 'miss'">
              {{ h.hit ? 'Попадание' : 'Мимо' }}
            </span>
        </td>

        <td>{{ fmtTime(h.createdAt) }}</td>
        <td>{{ h.scriptMicros }}</td>
      </tr>

      <tr v-if="hits.length === 0">
        <td colspan="7" style="color: var(--muted); padding: 14px;">История пуста</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>
