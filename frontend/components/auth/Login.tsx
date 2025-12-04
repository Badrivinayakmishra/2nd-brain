'use client'

import React, { useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'

export default function Login() {
  const [email, setEmail] = useState('')
  const router = useRouter()

  const handleLogin = () => {
    if (email) {
      // Store email in localStorage (no security for now)
      localStorage.setItem('userEmail', email)
      // Navigate to integrations page
      router.push('/integrations')
    }
  }

  const handleAccessKnowledge = () => {
    // Navigate to integrations without email
    router.push('/integrations')
  }

  return (
    <div 
      style={{
        width: '100vw',
        height: '100vh',
        backgroundColor: '#FFF3E4',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      {/* Logo at top left */}
      <div 
        style={{
          position: 'absolute',
          top: '32px',
          left: '32px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}
      >
        <div style={{ width: '41px', height: '51px', aspectRatio: '41/51' }}>
          <Image 
            src="/owl.png" 
            alt="2nd Brain Logo" 
            width={41} 
            height={51}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>
        <h1
          style={{
            width: '115px',
            height: '44px',
            color: '#081028',
            fontFamily: '"Work Sans", sans-serif',
            fontSize: '20px',
            fontWeight: 600,
            lineHeight: '22px'
          }}
        >
          2nd Brain
        </h1>
      </div>

      {/* Main content */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '40px' }}>
        {/* Two boxes */}
        <div style={{ display: 'flex', gap: '30px' }}>
          {/* Login Knowledge box */}
          <div
            onClick={handleLogin}
            style={{
              width: '243px',
              height: '80px',
              borderRadius: '8px',
              border: '0.6px solid rgba(52, 59, 79, 0.00)',
              backgroundColor: '#FFE2BF',
              boxShadow: '0 4px 4px 0 rgba(0, 0, 0, 0.25)',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '16px',
              cursor: 'pointer',
              transition: 'transform 0.2s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
          >
            <div
              style={{
                width: '39.816px',
                height: '40px',
                borderRadius: '80px',
                backgroundColor: 'rgba(39, 38, 106, 0.2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <div style={{ width: '25px', height: '22px', aspectRatio: '25/22' }}>
                <Image 
                  src="/login.png" 
                  alt="Login" 
                  width={25} 
                  height={22}
                  style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                />
              </div>
            </div>
            <div>
              <div
                style={{
                  width: '141px',
                  height: '31px',
                  color: '#081028',
                  fontFamily: '"Work Sans", sans-serif',
                  fontSize: '20px',
                  fontWeight: 500,
                  lineHeight: '18px'
                }}
              >
                Login Knowledge
              </div>
            </div>
          </div>

          {/* Access Knowledge box */}
          <div
            onClick={handleAccessKnowledge}
            style={{
              width: '243px',
              height: '80px',
              borderRadius: '8px',
              border: '0.6px solid rgba(52, 59, 79, 0.00)',
              backgroundColor: '#FFE2BF',
              boxShadow: '0 4px 4px 0 rgba(0, 0, 0, 0.25)',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '16px',
              cursor: 'pointer',
              transition: 'transform 0.2s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
          >
            <div
              style={{
                width: '39.816px',
                height: '40px',
                borderRadius: '80px',
                backgroundColor: 'rgba(39, 38, 106, 0.2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <div style={{ width: '25px', height: '22px', aspectRatio: '25/22' }}>
                <Image 
                  src="/access.png" 
                  alt="Access" 
                  width={25} 
                  height={22}
                  style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                />
              </div>
            </div>
            <div>
              <div
                style={{
                  width: '141px',
                  height: '31px',
                  color: '#081028',
                  fontFamily: '"Work Sans", sans-serif',
                  fontSize: '20px',
                  fontWeight: 500,
                  lineHeight: '18px'
                }}
              >
                Access Knowledge
              </div>
            </div>
          </div>
        </div>

        {/* Email input */}
        <div style={{ textAlign: 'center' }}>
          <p
            style={{
              color: '#081028',
              fontFamily: '"Work Sans", sans-serif',
              fontSize: '18px',
              fontWeight: 400,
              marginBottom: '16px'
            }}
          >
            Enter your email id...
          </p>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
            placeholder="your.email@company.com"
            style={{
              width: '400px',
              height: '50px',
              padding: '0 20px',
              borderRadius: '8px',
              border: '0.6px solid #7E89AC',
              backgroundColor: '#FFE2BF',
              fontSize: '16px',
              fontFamily: '"Work Sans", sans-serif',
              outline: 'none'
            }}
          />
        </div>
      </div>
    </div>
  )
}
