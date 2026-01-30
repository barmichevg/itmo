<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
  r: { type: Number, required: true },
  currentHit: { type: Object, default: null },
  hits: { type: Array, required: true },
  currentX: { type: Number, default: NaN },
  currentY: { type: Number, default: NaN },
  focusHitId: { type: [Number, String, null], default: null },
  focusOnly: { type: Boolean, default: false }
})

const emit = defineEmits(['pick'])

const canvasRef = ref(null)
const size = 320
const padding = 24

const pxPerUnit = computed(() => {
  const R = props.r > 0 ? props.r : 1
  return (size / 2 - padding) / R
})

function toCanvasX(x) {
  return size / 2 + x * pxPerUnit.value
}
function toCanvasY(y) {
  return size / 2 - y * pxPerUnit.value
}
function fromCanvas(px, py) {
  const x = (px - size / 2) / pxPerUnit.value
  const y = (size / 2 - py) / pxPerUnit.value
  return { x, y }
}

function clear(ctx) {
  ctx.clearRect(0, 0, size, size)
}

function drawAxes(ctx) {
  ctx.save()
  ctx.strokeStyle = 'rgba(148, 163, 184, 0.35)'
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(size/2, padding)
  ctx.lineTo(size/2, size-padding)
  ctx.moveTo(padding, size/2)
  ctx.lineTo(size-padding, size/2)
  ctx.stroke()


  ctx.fillStyle = 'rgba(148, 163, 184, 0.7)'
  ctx.font = '12px ui-sans-serif, system-ui'
  for (let t = -5; t <= 5; t++) {
    if (t === 0) continue
    const x = toCanvasX(t)
    const y = toCanvasY(t)

    if (x >= padding && x <= size-padding) {
      ctx.beginPath()
      ctx.moveTo(x, size/2 - 4)
      ctx.lineTo(x, size/2 + 4)
      ctx.stroke()
      ctx.fillText(String(t), x - 4, size/2 + 16)
    }

    if (y >= padding && y <= size-padding) {
      ctx.beginPath()
      ctx.moveTo(size/2 - 4, y)
      ctx.lineTo(size/2 + 4, y)
      ctx.stroke()
      ctx.fillText(String(t), size/2 + 8, y + 4)
    }
  }
  ctx.restore()
}

function drawArea(ctx) {
  const R = props.r
  if (!(R > 0)) return
  const rHalf = R / 2

  ctx.save()
  ctx.fillStyle = 'rgba(96, 165, 250, 0.18)'
  ctx.strokeStyle = 'rgba(96, 165, 250, 0.6)'
  ctx.lineWidth = 1

  // Q2
  ctx.beginPath()
  ctx.rect(toCanvasX(-rHalf), toCanvasY(R), rHalf * pxPerUnit.value, R * pxPerUnit.value)
  ctx.fill()
  ctx.stroke()

  // Q3
  ctx.beginPath()
  ctx.moveTo(toCanvasX(0), toCanvasY(0))
  ctx.lineTo(toCanvasX(-rHalf), toCanvasY(0))
  ctx.lineTo(toCanvasX(0), toCanvasY(-R))
  ctx.closePath()
  ctx.fill()
  ctx.stroke()

  // Q4
  ctx.beginPath()
  ctx.moveTo(toCanvasX(0), toCanvasY(0))
  ctx.arc(
      toCanvasX(0),
      toCanvasY(0),
      rHalf * pxPerUnit.value,
      0,
      Math.PI / 2,
      false
  )
  ctx.closePath()
  ctx.fill()
  ctx.stroke()

  ctx.restore()
}

function isInArea(x, y, R) {
  if (!(R > 0)) return false
  const rHalf = R / 2

  // Q2
  const rect =
      x <= 0 && y >= 0 &&
      x >= -rHalf && y <= R

  // Q4
  const circle =
      x >= 0 && y <= 0 &&
      (x * x + y * y) <= (rHalf * rHalf)

  // Q3
  const triangle =
      x <= 0 && y <= 0 &&
      x >= -rHalf &&
      (2 * x + y + R) >= 0

  return rect || circle || triangle
}

function drawHits(ctx) {
  ctx.save()

  const Rcur = props.r > 0 ? props.r : 1

  for (const h of props.hits) {
    const hx = Number(h.x)
    const hy = Number(h.y)
    const hr = Number(h.r)
    const ok = !!h.hit
    if (!Number.isFinite(hx) || !Number.isFinite(hy) || !Number.isFinite(hr) || hr === 0) continue

    const k = Rcur / hr
    const x = hx * k
    const y = hy * k

    const isActive = props.focusHitId != null && String(h.id) === String(props.focusHitId)
    if (props.focusOnly && !isActive) continue

    ctx.beginPath()
    ctx.fillStyle = ok ? 'rgba(52, 211, 153, 0.9)' : 'rgba(251, 113, 133, 0.9)'
    ctx.arc(toCanvasX(x), toCanvasY(y), isActive ? 6 : 4, 0, Math.PI * 2)
    ctx.fill()

    if (isActive) {
      ctx.strokeStyle = 'rgba(229, 231, 235, 0.95)'
      ctx.lineWidth = 2
      ctx.stroke()
    }
  }

  ctx.restore()
}


function drawCurrent(ctx) {
  if (props.focusOnly) return

  const h = props.currentHit
  if (!h) return

  const hx = Number(h.x)
  const hy = Number(h.y)
  const hr = Number(h.r)
  if (!Number.isFinite(hx) || !Number.isFinite(hy) || !Number.isFinite(hr) || hr === 0) return

  if (props.focusHitId != null && String(h.id) === String(props.focusHitId)) return

  const Rcur = props.r > 0 ? props.r : 1
  const k = Rcur / hr
  const x = hx * k
  const y = hy * k

  const ok = !!h.hit

  ctx.save()
  ctx.beginPath()
  ctx.fillStyle = ok ? 'rgba(52, 211, 153, 0.9)' : 'rgba(251, 113, 133, 0.9)'
  ctx.arc(toCanvasX(x), toCanvasY(y), 6, 0, Math.PI * 2)
  ctx.fill()

  ctx.strokeStyle = 'rgba(229, 231, 235, 0.95)'
  ctx.lineWidth = 2
  ctx.stroke()
  ctx.restore()
}



function redraw() {
  const c = canvasRef.value
  if (!c) return
  const ctx = c.getContext('2d')
  clear(ctx)
  drawArea(ctx)
  drawAxes(ctx)
  drawHits(ctx)
  drawCurrent(ctx)
}


function handleClick(ev) {
  const rect = ev.target.getBoundingClientRect()
  const px = ev.clientX - rect.left
  const py = ev.clientY - rect.top
  const { x, y } = fromCanvas(px, py)
  emit('pick', { x, y })
}

onMounted(redraw)
watch(() => [props.r, props.hits, props.focusHitId, props.focusOnly, props.currentHit], redraw, { deep: true })
</script>

<template>
  <div style="display:flex; justify-content:center;">
    <canvas
        ref="canvasRef"
        :width="size"
        :height="size"
        @click="handleClick"
        style="border: 1px solid var(--border); border-radius: 14px; background: var(--canvas-bg); cursor: crosshair;"
    />
  </div>
</template>
