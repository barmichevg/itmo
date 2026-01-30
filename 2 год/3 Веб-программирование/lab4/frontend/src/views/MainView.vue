<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import PlotCanvas from '../components/PlotCanvas.vue'
import HitTable from '../components/HitTable.vue'

const router = useRouter()

const me = ref(null)
const currentHit = ref(null)
const hits = ref([])
const loading = ref(false)
const error = ref('')

const x = ref('')
const y = ref('')
const r = ref('2')
const activeHitId = ref(null)
const focusOnly = ref(false)


function parseLocalNumber(str) {
  if (typeof str !== 'string') return NaN
  const s = str.trim()
  if (s.length === 0) return NaN
  const n = Number(s.replace(',', '.'))
  return Number.isFinite(n) ? n : NaN
}


function clientValidate({ skipXYRange = false } = {}) {
  const errors = []
  const xn = parseLocalNumber(x.value)
  const yn = parseLocalNumber(y.value)
  const rn = parseLocalNumber(r.value)

  if (!Number.isFinite(xn)) errors.push('X: введите число')
  if (!Number.isFinite(yn)) errors.push('Y: введите число')
  if (!Number.isFinite(rn)) errors.push('R: введите число')

  if (!skipXYRange) {
    if (Number.isFinite(xn) && (xn < -5 || xn > 5)) errors.push('X должен быть в диапазоне [-5; 5]')
    if (Number.isFinite(yn) && (yn < -5 || yn > 3)) errors.push('Y должен быть в диапазоне [-5; 3]')
  }
  if (Number.isFinite(rn) && (rn <= 0 || rn > 5)) errors.push('R должен быть в диапазоне (0; 5]')

  return { ok: errors.length === 0, rn, errors }
}

async function loadHits() {
  hits.value = await api.getHits()
  currentHit.value = hits.value.length ? hits.value[0] : null
}


async function submit({ fromGraph = false } = {}) {
  error.value = ''
  const v = clientValidate({ skipXYRange: fromGraph })
  if (!v.ok) {
    error.value = v.errors.join(' • ')
    return
  }
  loading.value = true
  try {
    const created = await api.createHit(x.value, y.value, r.value, fromGraph)
    hits.value = [created, ...hits.value]
    currentHit.value = created
    focusOnly.value = false
    activeHitId.value = null
  } catch (e) {
    if (e?.status === 401) {
      await router.replace('/')
      return
    }
    const msg = e?.data?.message || 'Ошибка при отправке точки'
    const errs = Array.isArray(e?.data?.errors) ? e.data.errors.join(' • ') : ''
    error.value = errs ? (msg + ': ' + errs) : msg
  } finally {
    loading.value = false
  }
}

async function clearHistory() {
  error.value = ''
  loading.value = true
  try {
    await api.clearHits()
    hits.value = []
    currentHit.value = null
    focusOnly.value = false
    activeHitId.value = null
  } catch (e) {
    error.value = e?.data?.message || 'Не удалось очистить историю'
  } finally {
    loading.value = false
  }
}

async function logout() {
  try { await api.logout() } catch {}
  await router.replace('/')
}

function viewHit(h) {
  activeHitId.value = h.id
  focusOnly.value = true

  // x.value = String(h.x)
  // y.value = String(h.y)
  // r.value = String(h.r)
}

function showAllPoints() {
  focusOnly.value = false
  activeHitId.value = null
}


function onPick({ x: px, y: py }) {
  x.value = (Math.round(px * 1000) / 1000).toString()
  y.value = (Math.round(py * 1000) / 1000).toString()
  submit({ fromGraph: true })
}

onMounted(async () => {
  try {
    me.value = await api.me()
  } catch {
    await router.replace('/')
    return
  }
  await loadHits()
})
</script>

<template>
  <div class="header">
    <h1>Бармичев Григорий Андреевич — P3210</h1>
    <small>Веб-программирование — ЛР4 — Вариант 123</small>
    <small v-if="me">Пользователь: <b>{{ me.login }}</b></small>
  </div>

  <div class="grid">
    <div class="card">
      <div class="row">
        <div class="field">
          <label>X (-5 … 5)</label>
          <input v-model="x" inputmode="decimal" placeholder="..." />
        </div>
        <div class="field">
          <label>Y (-5 … 3)</label>
          <input v-model="y" inputmode="decimal" placeholder="..." />
        </div>
        <div class="field">
          <label>R (0 … 5]</label>
          <input v-model="r" inputmode="decimal" placeholder="..." />
        </div>
      </div>

      <div class="row" style="margin-top: 12px;">
        <button class="button primary" :disabled="loading" @click="submit">Проверить</button>
        <button class="button primary" :disabled="loading" @click="clearHistory">Очистить историю</button>
        <button class="button danger" :disabled="loading" @click="logout">Выйти</button>
      </div>

      <div v-if="error" class="error">{{ error }}</div>
    </div>
    <div class="card">
      <PlotCanvas
          :r="parseLocalNumber(r) || 1"
          :hits="hits"
          :current-hit="currentHit"
          :focus-hit-id="activeHitId"
          :focus-only="focusOnly"
          @pick="onPick"
      />
      <div class="row" style="margin-top: 10px; justify-content:center;">
        <button class="button btnSmall" type="button" :disabled="!focusOnly" @click="showAllPoints">
          Показать все точки
        </button>
      </div>
    </div>
  </div>

  <div class="card">
    <h3 style="margin:0 0 10px;">История результатов</h3>
    <HitTable :hits="hits" :active-id="activeHitId" @view="viewHit" />
  </div>
</template>
