
import React, { useState } from 'react';

export default function AgricareAdvisoryLanding() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  function handleChange(e) {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (!form.name || !form.email || !form.message) {
      setError('Please fill all fields.');
      return;
    }
    // Placeholder: replace with real API call or form backend integration
    console.log('Contact form submitted', form);
    setSubmitted(true);
    setForm({ name: '', email: '', message: '' });
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white text-slate-800">
      {/* NAVBAR */}
      <header className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold">A</div>
          <div>
            <h1 className="text-lg font-semibold">Agricare Advisory</h1>
            <p className="text-xs text-slate-500">Smart farming · Sustainable yields</p>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-sm">
          <a href="#services" className="hover:text-emerald-600">Services</a>
          <a href="#how" className="hover:text-emerald-600">How it works</a>
          <a href="#resources" className="hover:text-emerald-600">Resources</a>
          <a href="#contact" className="hover:text-emerald-600">Contact</a>
          <a href="#" className="ml-4 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm">Get Started</a>
        </nav>

        <button className="md:hidden p-2 rounded-md bg-emerald-100">☰</button>
      </header>

      {/* HERO */}
      <section className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-8 items-center py-12">
        <div>
          <h2 className="text-3xl md:text-4xl font-extrabold leading-tight">Agricare Advisory — grow smarter, waste less</h2>
          <p className="mt-4 text-slate-600">Actionable crop advice, soil and pest guidance, irrigation recommendations and fertilizer planning — tailored for your farm, on your timeline.</p>

          <div className="mt-6 flex gap-4">
            <a href="#contact" className="px-5 py-3 bg-emerald-600 text-white rounded-lg font-medium">Talk to an expert</a>
            <a href="#services" className="px-5 py-3 border border-emerald-600 text-emerald-600 rounded-lg">See services</a>
          </div>

          <ul className="mt-6 grid grid-cols-2 gap-3 text-sm text-slate-600">
            <li>• Farmer-friendly recommendations</li>
            <li>• SMS & App alerts</li>
            <li>• Local language support</li>
            <li>• Weather-aware advisories</li>
          </ul>

          <div className="mt-6 text-xs text-slate-500">Trusted by smallholders & agri-businesses — practical advice, verified by experts.</div>
        </div>

        <div className="relative">
          <img src="https://images.unsplash.com/photo-1501004318641-b39e6451bec6?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=example" alt="farm" className="rounded-xl shadow-lg w-full h-80 object-cover"/>

          <div className="absolute -bottom-6 left-6 bg-white/90 rounded-lg p-4 shadow-md w-11/12 md:w-10/12">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-emerald-100 rounded-md flex items-center justify-center">🌾</div>
              <div>
                <div className="text-sm font-semibold">Free crop status check</div>
                <div className="text-xs text-slate-500">Send us a photo or field details and get a free initial assessment.</div>
              </div>
              <div className="ml-auto hidden sm:block">
                <a href="#contact" className="text-emerald-600 text-sm">Request now →</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SERVICES */}
      <section id="services" className="max-w-7xl mx-auto px-6 py-12">
        <h3 className="text-2xl font-bold">Our Services</h3>
        <p className="text-slate-600 mt-2">Comprehensive advisory built for real farms — practical, localised, and affordable.</p>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {title: 'Soil Testing & Fertility', desc: 'Detailed soil reports with fertilizer plans and nutrient management.'},
            {title: 'Pest & Disease Advisory', desc: 'Image-based diagnosis and treatment recommendations.'},
            {title: 'Irrigation & Water', desc: 'Optimised irrigation scheduling to save water and increase yields.'},
            {title: 'Crop Planning', desc: 'Seasonal crop selection and rotation planning.'},
            {title: 'Market Advisory', desc: 'Harvest timing and market price pointers for better returns.'},
            {title: 'Digital Farm Records', desc: 'Record keeping and analytics for farm decisions.'},
          ].map((s, i) => (
            <article key={i} className="bg-white rounded-xl p-5 shadow-sm">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-emerald-50 flex items-center justify-center font-bold text-emerald-700">{i+1}</div>
                <div>
                  <h4 className="font-semibold">{s.title}</h4>
                  <p className="text-sm text-slate-600 mt-2">{s.desc}</p>
                </div>
              </div>

              <div className="mt-4">
                <a href="#contact" className="text-emerald-600 text-sm">Get this service →</a>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="bg-emerald-50 py-12">
        <div className="max-w-6xl mx-auto px-6">
          <h3 className="text-2xl font-bold">How Agricare works</h3>
          <p className="text-slate-600 mt-2">Fast, affordable and localized advice in 3 simple steps.</p>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <div className="text-3xl">1</div>
              <h4 className="font-semibold mt-3">Share field details</h4>
              <p className="text-sm text-slate-600 mt-2">Upload photos, enter crop & soil details, or share coordinates.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <div className="text-3xl">2</div>
              <h4 className="font-semibold mt-3">Receive tailored plan</h4>
              <p className="text-sm text-slate-600 mt-2">We analyze and respond with a practical plan — including inputs and schedule.</p>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-sm">
              <div className="text-3xl">3</div>
              <h4 className="font-semibold mt-3">Follow up & support</h4>
              <p className="text-sm text-slate-600 mt-2">Monitoring and follow-up to ensure your crop stays on track.</p>
            </div>
          </div>
        </div>
      </section>

      {/* RESOURCES / TESTIMONIALS */}
      <section id="resources" className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid md:grid-cols-2 gap-8 items-start">
          <div>
            <h3 className="text-2xl font-bold">Resources & Case Studies</h3>
            <p className="text-slate-600 mt-2">Guides, crop calendars and success stories from farmers who used Agricare.</p>

            <ul className="mt-6 space-y-3">
              <li className="p-4 bg-white rounded-lg shadow-sm">
                <div className="font-semibold">Rice water management — case study</div>
                <div className="text-xs text-slate-500 mt-1">How optimized irrigation reduced water use by 28%.</div>
              </li>
              <li className="p-4 bg-white rounded-lg shadow-sm">
                <div className="font-semibold">Pest control without overuse of pesticide</div>
                <div className="text-xs text-slate-500 mt-1">Image diagnosis + targeted treatment plan.</div>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold">Farmer voices</h4>
            <div className="mt-4 space-y-4">
              <blockquote className="p-4 bg-emerald-50 rounded-lg">"Agricare's advice helped me plan fertilizer & increased yield by 15%." — Ramesh, Uttar Pradesh</blockquote>
              <blockquote className="p-4 bg-emerald-50 rounded-lg">"Quick response and simple steps — saved time and money." — Sita, Maharashtra</blockquote>
            </div>
          </div>
        </div>
      </section>

      {/* CONTACT */}
      <section id="contact" className="bg-white py-12">
        <div className="max-w-5xl mx-auto px-6 grid md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-2xl font-bold">Contact our Agri Experts</h3>
            <p className="text-slate-600 mt-2">Tell us about your farm and we’ll get back with a tailored plan. Free initial check.</p>

            <div className="mt-6 space-y-3 text-sm text-slate-600">
              <div>📞 +91 98765 43210</div>
              <div>✉️ hello@agricare.example</div>
              <div>📍 Serving farmers across regions</div>
            </div>

          </div>

          <div>
            <form onSubmit={handleSubmit} className="bg-emerald-50 p-6 rounded-lg">
              {submitted && <div className="mb-3 p-3 bg-emerald-100 text-emerald-800 rounded">Thanks — we'll contact you soon.</div>}
              {error && <div className="mb-3 p-3 bg-rose-100 text-rose-800 rounded">{error}</div>}

              <label className="block text-sm">Name</label>
              <input name="name" value={form.name} onChange={handleChange} className="w-full mt-1 p-2 rounded border" placeholder="Your name" />

              <label className="block text-sm mt-3">Email or Phone</label>
              <input name="email" value={form.email} onChange={handleChange} className="w-full mt-1 p-2 rounded border" placeholder="Email or mobile" />

              <label className="block text-sm mt-3">Message</label>
              <textarea name="message" value={form.message} onChange={handleChange} rows={4} className="w-full mt-1 p-2 rounded border" placeholder="Tell us about your crop/concern"></textarea>

              <div className="mt-4 flex items-center gap-3">
                <button type="submit" className="px-4 py-2 bg-emerald-600 text-white rounded">Send</button>
                <button type="button" onClick={()=>{setForm({name:'', email:'', message:''}); setError('');}} className="px-3 py-2 border rounded">Clear</button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="mt-12 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="font-semibold">Agricare Advisory</div>
            <div className="text-xs text-slate-300 mt-1">Practical farm advice — local experts.</div>
          </div>

          <div className="text-sm text-slate-300">© {new Date().getFullYear()} Agricare Advisory — All rights reserved</div>
        </div>
      </footer>
    </div>
    );
  }

  

  function sayHello() {
  alert("Hello! Your JavaScript is working 🚀");
}
