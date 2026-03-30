const https = require('https');

function fetch(url, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer fc-e0b993f54b8f495f997b5cd770cad96d',
        'Content-Length': Buffer.byteLength(data)
      }
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  const resp = await fetch('https://api.firecrawl.dev/v1/scrape', {
    url: 'https://shed.design/',
    formats: ['rawHtml'],
    waitFor: 3000
  });
  const j = JSON.parse(resp);
  const html = j.data?.rawHtml || '';

  // Strip out all <style> blocks to get clean HTML
  const clean = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');

  // Find home-hero section
  let idx = clean.indexOf('<section class="home-hero"');
  if (idx === -1) idx = clean.indexOf('class="home-hero"');
  if (idx > -1) {
    let start = clean.lastIndexOf('<', idx);
    console.log('=== HOME HERO HTML ===');
    console.log(clean.substring(start, start + 5000));
  } else {
    console.log('home-hero not found');
    // Just dump the body
    const bodyIdx = clean.indexOf('<body');
    if (bodyIdx > -1) {
      console.log('=== BODY START ===');
      console.log(clean.substring(bodyIdx, bodyIdx + 8000));
    }
  }
}

main().catch(console.error);
