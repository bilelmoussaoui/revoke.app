document.addEventListener(
  'DOMContentLoaded',
  function () {
    function search (pattern) {
      const $tiles = document.querySelectorAll('div.tile')
      $tiles.forEach($tile => {
        const title = $tile.querySelector('p.title').innerHTML
        if (title.toLowerCase().includes(pattern.toLowerCase())) {
          $tile.parentNode.style.display = 'block'
        } else {
          $tile.parentNode.style.display = 'none'
        }
      })
    }

    const $searchInput = document.querySelector('#searchInput')
    $searchInput.addEventListener('keyup', () => search($searchInput.value))
    $searchInput.addEventListener('change', () => search($searchInput.value))
  },
  false
)
