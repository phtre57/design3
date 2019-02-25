export default function timeFormat(ms) {
    let total = ms / 1000;

    const hh = parseInt( total / 3600, 10);
    total %= 3600;
    const mm = parseInt( total / 60, 10);
    const ss = parseInt( total % 60, 10);

    return ( addPadding(hh) + ":" + addPadding(mm) + ":" + addPadding(ss));
}

function addPadding(number, size = 2) {
    let s = String(number);
    while (s.length < size) { s = '0' + s;}
    return s;
  }