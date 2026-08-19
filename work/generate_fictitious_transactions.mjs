import fs from 'node:fs';
import path from 'node:path';

const sourcePath = path.resolve('data/outputs/result_test.csv');
const outputPath = path.resolve('data/outputs/result_test_500_ficticias.csv');
const sourceHeader = fs.readFileSync(sourcePath, 'utf8').split(/\r?\n/, 1)[0].replace(/^\uFEFF/, '').split(',');
const headers = [...sourceHeader, 'category'];

const incomeCategories = ['deposito', 'ganho de corrida', 'pagamento'];
const expenseCategories = ['outros', 'acessórios', 'alimentação', 'celular/chip', 'cnh', 'combustivel', 'financeamento', 'ipva', 'lavagem', 'manutenção', 'multas', 'pedagio e estacionamento', 'seguro'];
const expenseDescriptions = {
  'outros': 'Compra diversa', 'acessórios': 'Loja de acessórios automotivos', 'alimentação': 'Restaurante e lanchonete',
  'celular/chip': 'Recarga de celular', 'cnh': 'Taxa de habilitação CNH', 'combustivel': 'Posto de combustíveis',
  'financeamento': 'Parcela de financiamento', 'ipva': 'Pagamento de IPVA', 'lavagem': 'Lavagem automotiva',
  'manutenção': 'Manutenção e oficina', 'multas': 'Pagamento de multa',
  'pedagio e estacionamento': 'Pedágio e estacionamento', 'seguro': 'Parcela de seguro'
};

let seed = 20260819;
const random = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
const pick = (items) => items[Math.floor(random() * items.length)];
const pad = (n) => String(n).padStart(2, '0');
const quote = (value) => {
  const s = String(value ?? '');
  return /[",\r\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
};

let balance = 250000;
const rows = [];
for (let i = 0; i < 500; i++) {
  const d = new Date(Date.UTC(2025, 0, 1 + Math.floor(i * 1.45)));
  const date = d.toISOString().slice(0, 10);
  const day = pad(d.getUTCDate());
  const month = pad(d.getUTCMonth() + 1);
  const hour = pad(6 + Math.floor(random() * 17));
  const minute = pad(Math.floor(random() * 60));
  const isIncome = i % 7 === 0 || balance < 80000;
  const category = isIncome ? pick(incomeCategories) : pick(expenseCategories);
  const cents = isIncome ? 35000 + Math.floor(random() * 215001) : 1200 + Math.floor(random() * 73801);
  const signed = isIncome ? cents : -cents;
  balance += signed;
  const direction = isIncome ? 'credit' : 'debit';
  const transactionType = category === 'deposito' ? 'deposito' : (category === 'pagamento' ? 'transferencia' : 'pix');
  const description = isIncome
    ? (category === 'deposito' ? `Dep dinheiro ATM ${day}/${month} ${hour}:${minute} CENTRO`
      : category === 'ganho de corrida' ? `Pix - Recebido ${day}/${month} ${hour}:${minute} PLATAFORMA DE CORRIDAS`
      : `Transferência recebida ${day}/${month} ${hour}:${minute} PAGAMENTO DE SERVIÇO`)
    : `Pix - Enviado ${day}/${month} ${hour}:${minute} ${expenseDescriptions[category].toUpperCase()}`;
  const brAmount = (cents / 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const code = String(10000 + Math.floor(random() * 89999));
  const doc = String(700000000000000 + i * 997 + Math.floor(random() * 997));
  const raw = `${brAmount} (${isIncome ? '+' : '-'}) ${code} ${doc} ${description}`;
  const record = {
    date, description_raw: raw, description_normalized: description, amount_cents: signed,
    signed_amount_cents: signed, direction, transaction_type: transactionType,
    balance_after_cents: balance, doc_number: doc, transaction_code: code,
    source_page: 1 + Math.floor(i / 35), source_text: raw, extraction_method: 'synthetic',
    warnings: '', review_required: 'False', category
  };
  rows.push(headers.map((h) => quote(record[h])).join(','));
}

fs.writeFileSync(outputPath, [headers.join(','), ...rows].join('\r\n') + '\r\n', 'utf8');
console.log(outputPath);
